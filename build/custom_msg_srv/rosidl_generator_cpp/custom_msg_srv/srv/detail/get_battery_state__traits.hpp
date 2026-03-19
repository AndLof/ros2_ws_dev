// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msg_srv:srv/GetBatteryState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__TRAITS_HPP_
#define CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msg_srv/srv/detail/get_battery_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msg_srv
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetBatteryState_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetBatteryState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetBatteryState_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msg_srv

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_srv::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_srv::srv::GetBatteryState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_srv::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_srv::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_srv::srv::GetBatteryState_Request & msg)
{
  return custom_msg_srv::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_srv::srv::GetBatteryState_Request>()
{
  return "custom_msg_srv::srv::GetBatteryState_Request";
}

template<>
inline const char * name<custom_msg_srv::srv::GetBatteryState_Request>()
{
  return "custom_msg_srv/srv/GetBatteryState_Request";
}

template<>
struct has_fixed_size<custom_msg_srv::srv::GetBatteryState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_msg_srv::srv::GetBatteryState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_msg_srv::srv::GetBatteryState_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_msg_srv
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetBatteryState_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: battery_state
  {
    out << "battery_state: ";
    rosidl_generator_traits::value_to_yaml(msg.battery_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetBatteryState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: battery_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "battery_state: ";
    rosidl_generator_traits::value_to_yaml(msg.battery_state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetBatteryState_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msg_srv

namespace rosidl_generator_traits
{

[[deprecated("use custom_msg_srv::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msg_srv::srv::GetBatteryState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msg_srv::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msg_srv::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msg_srv::srv::GetBatteryState_Response & msg)
{
  return custom_msg_srv::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msg_srv::srv::GetBatteryState_Response>()
{
  return "custom_msg_srv::srv::GetBatteryState_Response";
}

template<>
inline const char * name<custom_msg_srv::srv::GetBatteryState_Response>()
{
  return "custom_msg_srv/srv/GetBatteryState_Response";
}

template<>
struct has_fixed_size<custom_msg_srv::srv::GetBatteryState_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_msg_srv::srv::GetBatteryState_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_msg_srv::srv::GetBatteryState_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msg_srv::srv::GetBatteryState>()
{
  return "custom_msg_srv::srv::GetBatteryState";
}

template<>
inline const char * name<custom_msg_srv::srv::GetBatteryState>()
{
  return "custom_msg_srv/srv/GetBatteryState";
}

template<>
struct has_fixed_size<custom_msg_srv::srv::GetBatteryState>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msg_srv::srv::GetBatteryState_Request>::value &&
    has_fixed_size<custom_msg_srv::srv::GetBatteryState_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msg_srv::srv::GetBatteryState>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msg_srv::srv::GetBatteryState_Request>::value &&
    has_bounded_size<custom_msg_srv::srv::GetBatteryState_Response>::value
  >
{
};

template<>
struct is_service<custom_msg_srv::srv::GetBatteryState>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msg_srv::srv::GetBatteryState_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msg_srv::srv::GetBatteryState_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__TRAITS_HPP_
