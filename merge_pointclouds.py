#!/usr/bin/env python3
"""
merge_pointclouds.py

Unisce due (o piu') PointCloud2 in un unico topic, trasformando ogni nuvola
in un frame comune (default: 'body') usando il TF tree.

Pensato per Spot: prende le nuvole prodotte da depthimage_to_pointcloud2 per
le camere frontright e frontleft e pubblica una nuvola unica gia' riallineata.

Esecuzione (ROS2 Humble):

    python3 merge_pointclouds.py --ros-args \
        -p input_topics:="['/frontright_pointcloud2','/frontleft_pointcloud2']" \
        -p output_topic:=/spot/pointcloud/merged \
        -p target_frame:=body \
        -p publish_rate:=10.0 \
        -p reliability:=best_effort   # usa 'reliable' se non arriva nulla

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
    serve, quindi lo eliminiamo a monte."""
    pts = pc2.read_points(cloud, field_names=('x', 'y', 'z'), skip_nans=False)
    return pc2.create_cloud_xyz32(cloud.header, pts.tolist())


class PointCloudMerger(Node):
    def __init__(self):
        super().__init__('pointcloud_merger')

        self.declare_parameter(
            'input_topics',
            ['/frontright_pointcloud2', '/frontleft_pointcloud2'])
        self.declare_parameter('output_topic', '/spot/pointcloud/merged')
        self.declare_parameter('target_frame', 'body')
        self.declare_parameter('publish_rate', 15.0)
        self.declare_parameter('tf_timeout', 0.1)
        # 'reliable' o 'best_effort'. I nodi depth di Spot pubblicano RELIABLE,
        # quindi se non arriva nulla in ingresso prova 'reliable'.
        self.declare_parameter('reliability', 'best_effort')

        self.input_topics = list(self.get_parameter('input_topics').value)
        self.output_topic = self.get_parameter('output_topic').value
        self.target_frame = self.get_parameter('target_frame').value
        rate = float(self.get_parameter('publish_rate').value)
        self.tf_timeout = float(self.get_parameter('tf_timeout').value)
        reliability_str = self.get_parameter('reliability').value.lower()

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

        self.latest = {}  # topic -> PointCloud2 gia' trasformata nel target_frame
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
            f"Merger avviato: {self.input_topics} -> {self.output_topic} "
            f"(frame comune: {self.target_frame})")

    def cloud_cb(self, msg, topic):
        # Cerca la trasformazione al timestamp della nuvola; se non c'e'
        # (es. TF leggermente in ritardo) ripiega sull'ultima disponibile.
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

        self.latest[topic] = do_transform_cloud(strip_to_xyz(msg), tf)

    def publish_merged(self):
        clouds = [c for c in self.latest.values() if c is not None]
        if not clouds:
            return
        merged = self.concat(clouds)
        if merged is not None:
            self.pub.publish(merged)

    def concat(self, clouds):
        ref = clouds[0]
        point_step = ref.point_step

        # Tutte le nuvole devono avere lo stesso layout di campi per la
        # concatenazione binaria diretta (qui e' garantito: stesso package,
        # stesso setting 'colorful').
        for c in clouds:
            if c.point_step != point_step or c.fields != ref.fields:
                self.get_logger().warn(
                    "Layout dei campi diverso tra le nuvole: merge saltato. "
                    "Assicurati che entrambe usino lo stesso 'colorful'.",
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