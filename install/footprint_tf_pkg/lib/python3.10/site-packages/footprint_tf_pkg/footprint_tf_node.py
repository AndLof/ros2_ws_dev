#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import tf2_ros
from geometry_msgs.msg import TransformStamped

import tf_transformations


class FootprintTF(Node):
    def __init__(self):
        super().__init__('body_footprint_tf')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # Timer a 20 Hz
        self.timer = self.create_timer(0.05, self.update_tf)

    def update_tf(self):
        try:
            # Lookup transform da map a body
            tf = self.tf_buffer.lookup_transform(
                'map',
                'body',
                rclpy.time.Time()
            )

            x = tf.transform.translation.x
            y = tf.transform.translation.y

            # Forza Z = 0
            z = 0.0

            # Estrai yaw dal quaternion
            q = tf.transform.rotation
            quat = [q.x, q.y, q.z, q.w]
            _, _, yaw = tf_transformations.euler_from_quaternion(quat)

            # Ricrea quaternion solo con yaw
            q_flat = tf_transformations.quaternion_from_euler(0.0, 0.0, yaw)

            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'map'
            t.child_frame_id = 'body_footprint'

            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = z

            t.transform.rotation.x = q_flat[0]
            t.transform.rotation.y = q_flat[1]
            t.transform.rotation.z = q_flat[2]
            t.transform.rotation.w = q_flat[3]

            self.tf_broadcaster.sendTransform(t)

        except Exception as e:
            self.get_logger().warn(f"TF lookup failed: {str(e)}")


def main():
    rclpy.init()
    node = FootprintTF()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
