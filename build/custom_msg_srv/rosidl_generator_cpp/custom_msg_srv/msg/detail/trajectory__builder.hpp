// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msg_srv:msg/Trajectory.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__BUILDER_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msg_srv/msg/detail/trajectory__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msg_srv
{

namespace msg
{

namespace builder
{

class Init_Trajectory_target_pose
{
public:
  Init_Trajectory_target_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msg_srv::msg::Trajectory target_pose(::custom_msg_srv::msg::Trajectory::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_srv::msg::Trajectory msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_srv::msg::Trajectory>()
{
  return custom_msg_srv::msg::builder::Init_Trajectory_target_pose();
}

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__BUILDER_HPP_
