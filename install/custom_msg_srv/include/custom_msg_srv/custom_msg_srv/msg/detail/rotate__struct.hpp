// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'rotation'
#include "std_msgs/msg/detail/float32__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_msg_srv__msg__Rotate __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_srv__msg__Rotate __declspec(deprecated)
#endif

namespace custom_msg_srv
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Rotate_
{
  using Type = Rotate_<ContainerAllocator>;

  explicit Rotate_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : rotation(_init)
  {
    (void)_init;
  }

  explicit Rotate_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : rotation(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _rotation_type =
    std_msgs::msg::Float32_<ContainerAllocator>;
  _rotation_type rotation;

  // setters for named parameter idiom
  Type & set__rotation(
    const std_msgs::msg::Float32_<ContainerAllocator> & _arg)
  {
    this->rotation = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_srv::msg::Rotate_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_srv::msg::Rotate_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::msg::Rotate_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::msg::Rotate_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_srv__msg__Rotate
    std::shared_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_srv__msg__Rotate
    std::shared_ptr<custom_msg_srv::msg::Rotate_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Rotate_ & other) const
  {
    if (this->rotation != other.rotation) {
      return false;
    }
    return true;
  }
  bool operator!=(const Rotate_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Rotate_

// alias to use template instance with default allocator
using Rotate =
  custom_msg_srv::msg::Rotate_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__ROTATE__STRUCT_HPP_
