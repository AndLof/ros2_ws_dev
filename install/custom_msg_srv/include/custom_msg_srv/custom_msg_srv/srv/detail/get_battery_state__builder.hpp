// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msg_srv:srv/GetBatteryState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__BUILDER_HPP_
#define CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msg_srv/srv/detail/get_battery_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msg_srv
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_srv::srv::GetBatteryState_Request>()
{
  return ::custom_msg_srv::srv::GetBatteryState_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace custom_msg_srv


namespace custom_msg_srv
{

namespace srv
{

namespace builder
{

class Init_GetBatteryState_Response_battery_state
{
public:
  Init_GetBatteryState_Response_battery_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msg_srv::srv::GetBatteryState_Response battery_state(::custom_msg_srv::srv::GetBatteryState_Response::_battery_state_type arg)
  {
    msg_.battery_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_srv::srv::GetBatteryState_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_srv::srv::GetBatteryState_Response>()
{
  return custom_msg_srv::srv::builder::Init_GetBatteryState_Response_battery_state();
}

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__BUILDER_HPP_
