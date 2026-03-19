// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msg_srv:srv/GetBatteryState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_HPP_
#define CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_msg_srv__srv__GetBatteryState_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_srv__srv__GetBatteryState_Request __declspec(deprecated)
#endif

namespace custom_msg_srv
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetBatteryState_Request_
{
  using Type = GetBatteryState_Request_<ContainerAllocator>;

  explicit GetBatteryState_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetBatteryState_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_srv__srv__GetBatteryState_Request
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_srv__srv__GetBatteryState_Request
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetBatteryState_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetBatteryState_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetBatteryState_Request_

// alias to use template instance with default allocator
using GetBatteryState_Request =
  custom_msg_srv::srv::GetBatteryState_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_msg_srv


#ifndef _WIN32
# define DEPRECATED__custom_msg_srv__srv__GetBatteryState_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_msg_srv__srv__GetBatteryState_Response __declspec(deprecated)
#endif

namespace custom_msg_srv
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetBatteryState_Response_
{
  using Type = GetBatteryState_Response_<ContainerAllocator>;

  explicit GetBatteryState_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->battery_state = 0.0f;
    }
  }

  explicit GetBatteryState_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->battery_state = 0.0f;
    }
  }

  // field types and members
  using _battery_state_type =
    float;
  _battery_state_type battery_state;

  // setters for named parameter idiom
  Type & set__battery_state(
    const float & _arg)
  {
    this->battery_state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msg_srv__srv__GetBatteryState_Response
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msg_srv__srv__GetBatteryState_Response
    std::shared_ptr<custom_msg_srv::srv::GetBatteryState_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetBatteryState_Response_ & other) const
  {
    if (this->battery_state != other.battery_state) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetBatteryState_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetBatteryState_Response_

// alias to use template instance with default allocator
using GetBatteryState_Response =
  custom_msg_srv::srv::GetBatteryState_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_msg_srv

namespace custom_msg_srv
{

namespace srv
{

struct GetBatteryState
{
  using Request = custom_msg_srv::srv::GetBatteryState_Request;
  using Response = custom_msg_srv::srv::GetBatteryState_Response;
};

}  // namespace srv

}  // namespace custom_msg_srv

#endif  // CUSTOM_MSG_SRV__SRV__DETAIL__GET_BATTERY_STATE__STRUCT_HPP_
