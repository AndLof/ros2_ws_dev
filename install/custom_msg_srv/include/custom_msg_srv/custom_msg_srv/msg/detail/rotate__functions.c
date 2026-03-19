// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from custom_msg_srv:msg/Rotate.idl
// generated code does not contain a copyright notice
#include "custom_msg_srv/msg/detail/rotate__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `rotation`
#include "std_msgs/msg/detail/float32__functions.h"

bool
custom_msg_srv__msg__Rotate__init(custom_msg_srv__msg__Rotate * msg)
{
  if (!msg) {
    return false;
  }
  // rotation
  if (!std_msgs__msg__Float32__init(&msg->rotation)) {
    custom_msg_srv__msg__Rotate__fini(msg);
    return false;
  }
  return true;
}

void
custom_msg_srv__msg__Rotate__fini(custom_msg_srv__msg__Rotate * msg)
{
  if (!msg) {
    return;
  }
  // rotation
  std_msgs__msg__Float32__fini(&msg->rotation);
}

bool
custom_msg_srv__msg__Rotate__are_equal(const custom_msg_srv__msg__Rotate * lhs, const custom_msg_srv__msg__Rotate * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // rotation
  if (!std_msgs__msg__Float32__are_equal(
      &(lhs->rotation), &(rhs->rotation)))
  {
    return false;
  }
  return true;
}

bool
custom_msg_srv__msg__Rotate__copy(
  const custom_msg_srv__msg__Rotate * input,
  custom_msg_srv__msg__Rotate * output)
{
  if (!input || !output) {
    return false;
  }
  // rotation
  if (!std_msgs__msg__Float32__copy(
      &(input->rotation), &(output->rotation)))
  {
    return false;
  }
  return true;
}

custom_msg_srv__msg__Rotate *
custom_msg_srv__msg__Rotate__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_msg_srv__msg__Rotate * msg = (custom_msg_srv__msg__Rotate *)allocator.allocate(sizeof(custom_msg_srv__msg__Rotate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(custom_msg_srv__msg__Rotate));
  bool success = custom_msg_srv__msg__Rotate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
custom_msg_srv__msg__Rotate__destroy(custom_msg_srv__msg__Rotate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    custom_msg_srv__msg__Rotate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
custom_msg_srv__msg__Rotate__Sequence__init(custom_msg_srv__msg__Rotate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_msg_srv__msg__Rotate * data = NULL;

  if (size) {
    data = (custom_msg_srv__msg__Rotate *)allocator.zero_allocate(size, sizeof(custom_msg_srv__msg__Rotate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = custom_msg_srv__msg__Rotate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        custom_msg_srv__msg__Rotate__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
custom_msg_srv__msg__Rotate__Sequence__fini(custom_msg_srv__msg__Rotate__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      custom_msg_srv__msg__Rotate__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

custom_msg_srv__msg__Rotate__Sequence *
custom_msg_srv__msg__Rotate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_msg_srv__msg__Rotate__Sequence * array = (custom_msg_srv__msg__Rotate__Sequence *)allocator.allocate(sizeof(custom_msg_srv__msg__Rotate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = custom_msg_srv__msg__Rotate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
custom_msg_srv__msg__Rotate__Sequence__destroy(custom_msg_srv__msg__Rotate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    custom_msg_srv__msg__Rotate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
custom_msg_srv__msg__Rotate__Sequence__are_equal(const custom_msg_srv__msg__Rotate__Sequence * lhs, const custom_msg_srv__msg__Rotate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!custom_msg_srv__msg__Rotate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
custom_msg_srv__msg__Rotate__Sequence__copy(
  const custom_msg_srv__msg__Rotate__Sequence * input,
  custom_msg_srv__msg__Rotate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(custom_msg_srv__msg__Rotate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    custom_msg_srv__msg__Rotate * data =
      (custom_msg_srv__msg__Rotate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!custom_msg_srv__msg__Rotate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          custom_msg_srv__msg__Rotate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!custom_msg_srv__msg__Rotate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
