// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__BUILDER_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msg_srv/msg/detail/rotate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msg_srv
{

namespace msg
{

namespace builder
{

class Init_Rotate_rotation
{
public:
  Init_Rotate_rotation()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msg_srv::msg::Rotate rotation(::custom_msg_srv::msg::Rotate::_rotation_type arg)
  {
    msg_.rotation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msg_srv::msg::Rotate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msg_srv::msg::Rotate>()
{
  return custom_msg_srv::msg::builder::Init_Rotate_rotation();
}

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__BUILDER_HPP_
