// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msg_srv:msg/Trajectory.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__TRAITS_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msg_srv/msg/detail/trajectory__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace custom_msg_srv
{

namespace msg
{

inline void to_flow_style_yaml(
  const Trajectory & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_pose
  {
    out << "target_pose: ";
    to_flow_style_yaml(msg.target_pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Trajectory & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_pose:\n";
    to_block_style_yaml(msg.target_pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Trajectory & msg, bool use_flow_style = false)
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
  const custom_msg_srv::msg::Trajectory & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_srv::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_srv::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_srv::msg::Trajectory & msg)
{
  return custom_msg_srv::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_srv::msg::Trajectory>()
{
  return "custom_msg_srv::msg::Trajectory";
}

template<>
inline const char * name<custom_msg_srv::msg::Trajectory>()
{
  return "custom_msg_srv/msg/Trajectory";
}

template<>
struct has_fixed_size<custom_msg_srv::msg::Trajectory>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct has_bounded_size<custom_msg_srv::msg::Trajectory>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::PoseStamped>::value> {};

template<>
struct is_message<custom_msg_srv::msg::Trajectory>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__TRAITS_HPP_
