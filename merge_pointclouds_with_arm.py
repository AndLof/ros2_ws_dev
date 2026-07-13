#!/usr/bin/env python3
"""
merge_pointclouds.py

Unisce N PointCloud2 in un unico topic, trasformando ogni nuvola in un frame
comune usando il TF tree.

Pensato per Spot: prende le nuvole prodotte da depthimage_to_pointcloud2 per
le camere frontright, frontleft e la RGBD del braccio, e pubblica una nuvola
unica gia' riallineata.

Esecuzione (ROS2 Humble):

    python3 merge_pointclouds.py --ros-args \
        -p input_topics:="['/frontright_pointcloud2','/frontleft_pointcloud2','/arm_pointcloud2']" \
        -p output_topic:=/spot/pointcloud/merged \
        -p target_frame:=spot_body \
        -p publish_rate:=10.0 \
        -p reliability:=reliable \
        -p max_cloud_age:=2.0

Parametri:
    input_topics   lista dei topic PointCloud2 da unire (qualsiasi numero)
    output_topic   topic della nuvola unita
    target_frame   frame comune in cui riportare tutti i punti
    publish_rate   Hz di pubblicazione della nuvola unita
    reliability    'reliable' o 'best_effort' (vale per input e output)
    tf_timeout     attesa massima per la TF al timestamp della nuvola
    max_cloud_age  secondi oltre i quali una nuvola e' considerata obsoleta
                   e viene esclusa dal merge. 0 = disabilitato.

Dipendenze (gia' presenti in un'installazione ros-humble-desktop):
    ros-humble-tf2-ros, ros-humble-tf2-sensor-msgs
"""

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.time import Time
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import PointCloud2
import tf2_ros
from tf2_ros import TransformException

from sensor_msgs_py import point_cloud2 as pc2

# In Humble la funzione sta in tf2_sensor_msgs.tf2_sensor_msgs;
# il fallback copre eventuali layout diversi del pacchetto.
try:
    from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
except ImportError:
    from tf2_sensor_msgs import do_transform_cloud


def strip_to_xyz(cloud):
    """Restituisce una copia della nuvola con i soli campi x, y, z.

    Le nuvole prodotte con colorful:=true contengono anche il campo 'rgb',
    che manda in errore do_transform_cloud su Humble. Il colore qui non
    serve, quindi lo eliminiamo a monte.

    Questo normalizza anche il layout dei campi: nuvole provenienti da
    sensori diversi diventano tutte xyz32, quindi concatenabili."""
    pts = pc2.read_points(cloud, field_names=('x', 'y', 'z'), skip_nans=False)
    return pc2.create_cloud_xyz32(cloud.header, pts.tolist())


class PointCloudMerger(Node):
    def __init__(self):
        super().__init__('pointcloud_merger')

        self.declare_parameter(
            'input_topics',
            ['/frontright_pointcloud2',
             '/frontleft_pointcloud2',
             '/arm_pointcloud2'])
        self.declare_parameter('output_topic', '/spot/pointcloud/merged')
        self.declare_parameter('target_frame', 'spot_body')
        self.declare_parameter('publish_rate', 10.0)
        self.declare_parameter('tf_timeout', 0.1)
        # 'reliable' o 'best_effort'. I nodi depth di Spot pubblicano RELIABLE.
        self.declare_parameter('reliability', 'best_effort')
        # Una nuvola piu' vecchia di max_cloud_age secondi viene esclusa dal
        # merge: evita di pianificare attorno a ostacoli non piu' aggiornati
        # quando una sorgente si ferma o perde frame. 0 = disabilitato.
        self.declare_parameter('max_cloud_age', 2.0)

        self.input_topics = list(self.get_parameter('input_topics').value)
        self.output_topic = self.get_parameter('output_topic').value
        self.target_frame = self.get_parameter('target_frame').value
        rate = float(self.get_parameter('publish_rate').value)
        self.tf_timeout = float(self.get_parameter('tf_timeout').value)
        reliability_str = self.get_parameter('reliability').value.lower()
        self.max_cloud_age = float(self.get_parameter('max_cloud_age').value)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        reliability = (ReliabilityPolicy.RELIABLE
                       if reliability_str == 'reliable'
                       else ReliabilityPolicy.BEST_EFFORT)
        sensor_qos = QoSProfile(
            reliability=reliability,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )

        # topic -> (PointCloud2 gia' nel target_frame, istante di ricezione)
        self.latest = {}
        self.subs = []
        for topic in self.input_topics:
            sub = self.create_subscription(
                PointCloud2, topic,
                lambda msg, t=topic: self.cloud_cb(msg, t),
                sensor_qos)
            self.subs.append(sub)

        self.pub = self.create_publisher(PointCloud2, self.output_topic, sensor_qos)
        self.timer = self.create_timer(1.0 / rate, self.publish_merged)

        self.get_logger().info(
            f"Merger avviato: {len(self.input_topics)} sorgenti "
            f"{self.input_topics} -> {self.output_topic} "
            f"(frame comune: {self.target_frame}, "
            f"max_cloud_age: {self.max_cloud_age}s)")

    def cloud_cb(self, msg, topic):
        # Cerca la trasformazione al timestamp della nuvola; se non c'e'
        # (es. TF leggermente in ritardo) ripiega sull'ultima disponibile.
        # Per la camera del braccio, che si muove, la TF al timestamp esatto
        # e' importante: il fallback introduce errore se il braccio si muove.
        try:
            tf = self.tf_buffer.lookup_transform(
                self.target_frame, msg.header.frame_id,
                msg.header.stamp,
                timeout=Duration(seconds=self.tf_timeout))
        except TransformException:
            try:
                tf = self.tf_buffer.lookup_transform(
                    self.target_frame, msg.header.frame_id, Time())
            except TransformException as e:
                self.get_logger().warn(
                    f"TF {self.target_frame} <- {msg.header.frame_id} non "
                    f"disponibile ({topic}): {e}",
                    throttle_duration_sec=2.0)
                return

        transformed = do_transform_cloud(strip_to_xyz(msg), tf)
        self.latest[topic] = (transformed, self.get_clock().now())

    def fresh_clouds(self):
        """Nuvole non obsolete, in ordine di input_topics."""
        now = self.get_clock().now()
        clouds = []
        for topic in self.input_topics:
            entry = self.latest.get(topic)
            if entry is None:
                continue
            cloud, stamp = entry
            if self.max_cloud_age > 0.0:
                age = (now - stamp).nanoseconds * 1e-9
                if age > self.max_cloud_age:
                    self.get_logger().warn(
                        f"Nuvola da {topic} obsoleta ({age:.1f}s): esclusa "
                        f"dal merge.",
                        throttle_duration_sec=5.0)
                    continue
            clouds.append(cloud)
        return clouds

    def publish_merged(self):
        clouds = self.fresh_clouds()
        if not clouds:
            return
        merged = self.concat(clouds)
        if merged is not None:
            self.pub.publish(merged)

    def concat(self, clouds):
        ref = clouds[0]
        point_step = ref.point_step

        # Dopo strip_to_xyz tutte le nuvole sono xyz32, quindi il layout
        # coincide sempre. Il controllo resta come rete di sicurezza.
        for c in clouds:
            if c.point_step != point_step or c.fields != ref.fields:
                self.get_logger().warn(
                    "Layout dei campi diverso tra le nuvole: merge saltato.",
                    throttle_duration_sec=5.0)
                return None

        data = bytearray()
        total_points = 0
        for c in clouds:
            n_points = c.width * c.height
            if c.row_step == c.point_step * c.width:
                data.extend(bytes(c.data))           # caso normale, nessun padding
            else:
                raw = bytes(c.data)                  # rimuove eventuale padding di riga
                valid = c.point_step * c.width
                for r in range(c.height):
                    start = r * c.row_step
                    data.extend(raw[start:start + valid])
            total_points += n_points

        merged = PointCloud2()
        merged.header.stamp = self.get_clock().now().to_msg()
        merged.header.frame_id = self.target_frame
        merged.fields = ref.fields
        merged.is_bigendian = ref.is_bigendian
        merged.point_step = point_step
        merged.height = 1
        merged.width = total_points
        merged.row_step = point_step * total_points
        merged.data = bytes(data)
        merged.is_dense = False
        return merged


def main():
    rclpy.init()
    node = PointCloudMerger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
