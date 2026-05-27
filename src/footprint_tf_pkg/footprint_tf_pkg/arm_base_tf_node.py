#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import tf2_ros
from geometry_msgs.msg import TransformStamped


class SpotArmMountTF(Node):
    def __init__(self):
        super().__init__('spot_arm_mount_tf')

        # Static TF broadcaster
        self.tf_broadcaster = tf2_ros.StaticTransformBroadcaster(self)

        # Parameters
        self.declare_parameter('parent_frame', 'spot_body')

        # IMPORTANT:
        # use the REAL base frame of your arm
        self.declare_parameter('child_frame', 'base_link')

        # Mount position of the arm on Spot
        self.declare_parameter('x', 0.3)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('z', 0.0)

        # Mount orientation quaternion
        self.declare_parameter('qx', 0.0)
        self.declare_parameter('qy', 0.0)
        self.declare_parameter('qz', 0.0)
        self.declare_parameter('qw', 1.0)

        self.publish_static_transform()

    def publish_static_transform(self):

        t = TransformStamped()

        # Timestamp
        t.header.stamp = self.get_clock().now().to_msg()

        # Frames
        t.header.frame_id = self.get_parameter('parent_frame').value
        t.child_frame_id = self.get_parameter('child_frame').value

        # Translation
        t.transform.translation.x = self.get_parameter('x').value
        t.transform.translation.y = self.get_parameter('y').value
        t.transform.translation.z = self.get_parameter('z').value

        # Rotation
        t.transform.rotation.x = self.get_parameter('qx').value
        t.transform.rotation.y = self.get_parameter('qy').value
        t.transform.rotation.z = self.get_parameter('qz').value
        t.transform.rotation.w = self.get_parameter('qw').value

        # Publish static TF
        self.tf_broadcaster.sendTransform(t)

        self.get_logger().info(
            f"Published static TF: "
            f"{t.header.frame_id} -> {t.child_frame_id}"
        )


def main():
    rclpy.init()

    node = SpotArmMountTF()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
