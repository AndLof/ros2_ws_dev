// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "custom_msg_srv/msg/detail/rotate__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace custom_msg_srv
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Rotate_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) custom_msg_srv::msg::Rotate(_init);
}

void Rotate_fini_function(void * message_memory)
{
  auto typed_message = static_cast<custom_msg_srv::msg::Rotate *>(message_memory);
  typed_message->~Rotate();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Rotate_message_member_array[1] = {
  {
    "rotation",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Float32>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_msg_srv::msg::Rotate, rotation),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Rotate_message_members = {
  "custom_msg_srv::msg",  // message namespace
  "Rotate",  // message name
  1,  // number of fields
  sizeof(custom_msg_srv::msg::Rotate),
  Rotate_message_member_array,  // message members
  Rotate_init_function,  // function to initialize message memory (memory has to be allocated)
  Rotate_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Rotate_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Rotate_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace custom_msg_srv


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_msg_srv::msg::Rotate>()
{
  return &::custom_msg_srv::msg::rosidl_typesupport_introspection_cpp::Rotate_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_msg_srv, msg, Rotate)() {
  return &::custom_msg_srv::msg::rosidl_typesupport_introspection_cpp::Rotate_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
