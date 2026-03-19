// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_H_
#define CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'rotation'
#include "std_msgs/msg/detail/float32__struct.h"

/// Struct defined in msg/Rotate in the package custom_msg_srv.
typedef struct custom_msg_srv__msg__Rotate
{
  std_msgs__msg__Float32 rotation;
} custom_msg_srv__msg__Rotate;

// Struct for a sequence of custom_msg_srv__msg__Rotate.
typedef struct custom_msg_srv__msg__Rotate__Sequence
{
  custom_msg_srv__msg__Rotate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_srv__msg__Rotate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_H_
