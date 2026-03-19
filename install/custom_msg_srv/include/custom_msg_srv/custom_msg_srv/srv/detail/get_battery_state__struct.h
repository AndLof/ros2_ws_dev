// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msg_srv:srv/GetBatteryState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_H_
#define CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetBatteryState in the package custom_msg_srv.
typedef struct custom_msg_srv__srv__GetBatteryState_Request
{
  uint8_t structure_needs_at_least_one_member;
} custom_msg_srv__srv__GetBatteryState_Request;

// Struct for a sequence of custom_msg_srv__srv__GetBatteryState_Request.
typedef struct custom_msg_srv__srv__GetBatteryState_Request__Sequence
{
  custom_msg_srv__srv__GetBatteryState_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_srv__srv__GetBatteryState_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/GetBatteryState in the package custom_msg_srv.
typedef struct custom_msg_srv__srv__GetBatteryState_Response
{
  float battery_state;
} custom_msg_srv__srv__GetBatteryState_Response;

// Struct for a sequence of custom_msg_srv__srv__GetBatteryState_Response.
typedef struct custom_msg_srv__srv__GetBatteryState_Response__Sequence
{
  custom_msg_srv__srv__GetBatteryState_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msg_srv__srv__GetBatteryState_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_H_
