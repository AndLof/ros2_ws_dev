// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from custom_msg_srv:srv/GetBatteryState.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "custom_msg_srv/srv/detail/get_battery_state__struct.h"
#include "custom_msg_srv/srv/detail/get_battery_state__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_srv
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetBatteryState_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetBatteryState_Request_type_support_ids_t;

static const _GetBatteryState_Request_type_support_ids_t _GetBatteryState_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetBatteryState_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetBatteryState_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetBatteryState_Request_type_support_symbol_names_t _GetBatteryState_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_srv, srv, GetBatteryState_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_srv, srv, GetBatteryState_Request)),
  }
};

typedef struct _GetBatteryState_Request_type_support_data_t
{
  void * data[2];
} _GetBatteryState_Request_type_support_data_t;

static _GetBatteryState_Request_type_support_data_t _GetBatteryState_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetBatteryState_Request_message_typesupport_map = {
  2,
  "custom_msg_srv",
  &_GetBatteryState_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GetBatteryState_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GetBatteryState_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetBatteryState_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetBatteryState_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_srv

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_srv, srv, GetBatteryState_Request)() {
  return &::custom_msg_srv::srv::rosidl_typesupport_c::GetBatteryState_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_msg_srv/srv/detail/get_battery_state__struct.h"
// already included above
// #include "custom_msg_srv/srv/detail/get_battery_state__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_srv
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetBatteryState_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetBatteryState_Response_type_support_ids_t;

static const _GetBatteryState_Response_type_support_ids_t _GetBatteryState_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetBatteryState_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetBatteryState_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetBatteryState_Response_type_support_symbol_names_t _GetBatteryState_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_srv, srv, GetBatteryState_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_srv, srv, GetBatteryState_Response)),
  }
};

typedef struct _GetBatteryState_Response_type_support_data_t
{
  void * data[2];
} _GetBatteryState_Response_type_support_data_t;

static _GetBatteryState_Response_type_support_data_t _GetBatteryState_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetBatteryState_Response_message_typesupport_map = {
  2,
  "custom_msg_srv",
  &_GetBatteryState_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GetBatteryState_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GetBatteryState_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetBatteryState_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetBatteryState_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_srv

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_srv, srv, GetBatteryState_Response)() {
  return &::custom_msg_srv::srv::rosidl_typesupport_c::GetBatteryState_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_msg_srv/srv/detail/get_battery_state__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_msg_srv
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetBatteryState_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetBatteryState_type_support_ids_t;

static const _GetBatteryState_type_support_ids_t _GetBatteryState_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetBatteryState_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetBatteryState_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetBatteryState_type_support_symbol_names_t _GetBatteryState_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_msg_srv, srv, GetBatteryState)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_msg_srv, srv, GetBatteryState)),
  }
};

typedef struct _GetBatteryState_type_support_data_t
{
  void * data[2];
} _GetBatteryState_type_support_data_t;

static _GetBatteryState_type_support_data_t _GetBatteryState_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetBatteryState_service_typesupport_map = {
  2,
  "custom_msg_srv",
  &_GetBatteryState_service_typesupport_ids.typesupport_identifier[0],
  &_GetBatteryState_service_typesupport_symbol_names.symbol_name[0],
  &_GetBatteryState_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GetBatteryState_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetBatteryState_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_msg_srv

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, custom_msg_srv, srv, GetBatteryState)() {
  return &::custom_msg_srv::srv::rosidl_typesupport_c::GetBatteryState_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
