#!/usr/bin/env python3
"""
person_detector_node.py
-----------------------
Nodo ROS2 (Humble) che esegue Ultralytics YOLO su uno stream di immagini RGB
(es. la camera del braccio Kinova) per rilevare persone (ed eventualmente altre
classi COCO, come una palla). Pubblica:

  - /person_detected  (std_msgs/Bool)   True se c'e' almeno una persona in vista
  - /person_count     (std_msgs/Int32)  numero di persone nel frame
  - /yolo/annotated   (sensor_msgs/Image) immagine con i box disegnati (debug)

Parametri principali (override da CLI o launch file):
  image_topic        topic della camera RGB da leggere
  model_path         file dei pesi (es. yolo26n.pt, yolo11n.pt)
  conf               soglia di confidenza minima (0-1)
  classes            lista di id classe COCO da tenere (0 = person, 32 = sports ball)
  device             "cpu" oppure "0" per la prima GPU
  publish_annotated  se True pubblica l'immagine annotata
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image
from std_msgs.msg import Bool, Int32
from cv_bridge import CvBridge

from ultralytics import YOLO


class PersonDetector(Node):
    def __init__(self):
        super().__init__("person_detector")

        # ---- Parametri ----
        self.declare_parameter("image_topic", "/camera/color/image_raw")
        self.declare_parameter("model_path", "yolo26n.pt")
        self.declare_parameter("conf", 0.5)
        self.declare_parameter("classes", [0])       # 0 = person
        self.declare_parameter("device", "cpu")      # "cpu" oppure "0" per GPU
        self.declare_parameter("publish_annotated", True)

        image_topic = self.get_parameter("image_topic").value
        model_path = self.get_parameter("model_path").value
        self.conf = self.get_parameter("conf").value
        self.classes = list(self.get_parameter("classes").value)
        self.device = self.get_parameter("device").value
        self.publish_annotated = self.get_parameter("publish_annotated").value

        # ---- Carica il modello UNA VOLTA SOLA (non a ogni frame!) ----
        self.get_logger().info(
            f"Carico il modello YOLO: {model_path} su device '{self.device}'"
        )
        self.model = YOLO(model_path)

        self.bridge = CvBridge()

        # ---- Subscriber / Publisher ----
        # QoS "sensor_data" = BEST_EFFORT, coerente con la maggior parte dei
        # driver di camera. Se non la imposti, spesso NON ricevi le immagini.
        self.sub = self.create_subscription(
            Image, image_topic, self.image_callback, qos_profile_sensor_data
        )
        self.person_pub = self.create_publisher(Bool, "person_detected", 10)
        self.count_pub = self.create_publisher(Int32, "person_count", 10)
        if self.publish_annotated:
            self.annotated_pub = self.create_publisher(Image, "yolo/annotated", 10)

        self._busy = False  # semplice guardia per scartare i frame in eccesso
        self.get_logger().info(
            f"In ascolto su '{image_topic}'. Attendo immagini..."
        )

    def image_callback(self, msg: Image):
        # Se stiamo ancora elaborando il frame precedente, scartiamo questo:
        # su CPU l'inferenza e' piu' lenta del frame rate della camera e a noi
        # interessa solo la vista piu' recente, non ogni singolo frame.
        if self._busy:
            return
        self._busy = True
        try:
            # ROS Image -> OpenCV (BGR, la convenzione usata da OpenCV/YOLO).
            # Se la camera pubblica in rgb8, cv_bridge converte comunque in bgr8.
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            results = self.model(
                frame,
                conf=self.conf,
                classes=self.classes,
                device=self.device,
                verbose=False,
            )
            r = results[0]

            # Conta quante detection sono "person" (classe 0)
            n_person = 0
            if r.boxes is not None and len(r.boxes) > 0:
                n_person = int((r.boxes.cls == 0).sum().item())

            self.person_pub.publish(Bool(data=(n_person > 0)))
            self.count_pub.publish(Int32(data=n_person))

            if n_person > 0:
                self.get_logger().info(f"{n_person} persona/e rilevata/e")

            if self.publish_annotated:
                annotated = r.plot()  # immagine BGR con box + etichette
                out = self.bridge.cv2_to_imgmsg(annotated, encoding="bgr8")
                out.header = msg.header
                self.annotated_pub.publish(out)

        except Exception as e:
            self.get_logger().error(f"Inferenza fallita: {e}")
        finally:
            self._busy = False


def main(args=None):
    rclpy.init(args=args)
    node = PersonDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
