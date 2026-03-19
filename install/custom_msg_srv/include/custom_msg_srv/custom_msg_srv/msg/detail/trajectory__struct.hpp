// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msg_srv:msg/Trajectory.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_HPP_
#define CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_msg_srv__msg__Trajectory __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_srv__msg__Trajectory __declspec(deprecated)
#endif

namespace custom_msg_srv
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Trajectory_
{
  using Type = Trajectory_<ContainerAllocator>;

  explicit Trajectory_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_init)
  {
    (void)_init;
  }

  explicit Trajectory_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _target_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _target_pose_type target_pose;

  // setters for named parameter idiom
  Type & set__target_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->target_pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_srv::msg::Trajectory_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_srv::msg::Trajectory_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::msg::Trajectory_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::msg::Trajectory_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_srv__msg__Trajectory
    std::shared_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_srv__msg__Trajectory
    std::shared_ptr<custom_msg_srv::msg::Trajectory_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Trajectory_ & other) const
  {
    if (this->target_pose != other.target_pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const Trajectory_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Trajectory_

// alias to use template instance with default allocator
using Trajectory =
  custom_msg_srv::msg::Trajectory_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__MSG__DETAIL__TRAJECTORY__STRUCT_HPP_
