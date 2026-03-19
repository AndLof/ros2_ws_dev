// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msg_srv:msg/Trajectory.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_H_
#define CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in msg/Trajectory in the package custom_msg_srv.
typedef struct custom_msg_srv__msg__Trajectory
{
  geometry_msgs__msg__PoseStamped target_pose;
} custom_msg_srv__msg__Trajectory;

// Struct for a sequence of custom_msg_srv__msg__Trajectory.
typedef struct custom_msg_srv__msg__Trajectory__Sequence
{
  custom_msg_srv__msg__Trajectory * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_srv__msg__Trajectory__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_H_
