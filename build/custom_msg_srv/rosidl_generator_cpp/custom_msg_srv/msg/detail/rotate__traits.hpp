// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__TRAITS_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msg_srv/msg/detail/rotate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'rotation'
#include "std_msgs/msg/detail/float32__traits.hpp"

namespace custom_msg_srv
{

namespace msg
{

inline void to_flow_style_yaml(
  const Rotate & msg,
  std::ostream & out)
{
  out << "{";
  // member: rotation
  {
    out << "rotation: ";
    to_flow_style_yaml(msg.rotation, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Rotate & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: rotation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rotation:\n";
    to_block_style_yaml(msg.rotation, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Rotate & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_msg_srv

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_srv::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_srv::msg::Rotate & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_srv::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_srv::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_srv::msg::Rotate & msg)
{
  return custom_msg_srv::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_srv::msg::Rotate>()
{
  return "custom_msg_srv::msg::Rotate";
}

template<>
inline const char * name<custom_msg_srv::msg::Rotate>()
{
  return "custom_msg_srv/msg/Rotate";
}

template<>
struct has_fixed_size<custom_msg_srv::msg::Rotate>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Float32>::value> {};

template<>
struct has_bounded_size<custom_msg_srv::msg::Rotate>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Float32>::value> {};

template<>
struct is_message<custom_msg_srv::msg::Rotate>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__TRAITS_HPP_
