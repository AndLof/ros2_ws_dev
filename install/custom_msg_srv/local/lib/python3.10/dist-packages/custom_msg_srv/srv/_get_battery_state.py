# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_msg_srv:srv/GetBatteryState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetBatteryState_Request(type):
    """Metaclass of message 'GetBatteryState_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_msg_srv')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_msg_srv.srv.GetBatteryState_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_battery_state__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_battery_state__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_battery_state__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_battery_state__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_battery_state__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetBatteryState_Request(metaclass=Metaclass_GetBatteryState_Request):
    """Message class 'GetBatteryState_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetBatteryState_Response(type):
    """Metaclass of message 'GetBatteryState_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_msg_srv')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_msg_srv.srv.GetBatteryState_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_battery_state__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_battery_state__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_battery_state__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_battery_state__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_battery_state__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetBatteryState_Response(metaclass=Metaclass_GetBatteryState_Response):
    """Message class 'GetBatteryState_Response'."""

    __slots__ = [
        '_battery_state',
    ]

    _fields_and_field_types = {
        'battery_state': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.battery_state = kwargs.get('battery_state', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.battery_state != other.battery_state:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def battery_state(self):
        """Message field 'battery_state'."""
        return self._battery_state

    @battery_state.setter
    def battery_state(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery_state' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery_state' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery_state = value


class Metaclass_GetBatteryState(type):
    """Metaclass of service 'GetBatteryState'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_msg_srv')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_msg_srv.srv.GetBatteryState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_battery_state

            from custom_msg_srv.srv import _get_battery_state
            if _get_battery_state.Metaclass_GetBatteryState_Request._TYPE_SUPPORT is None:
                _get_battery_state.Metaclass_GetBatteryState_Request.__import_type_support__()
            if _get_battery_state.Metaclass_GetBatteryState_Response._TYPE_SUPPORT is None:
                _get_battery_state.Metaclass_GetBatteryState_Response.__import_type_support__()


class GetBatteryState(metaclass=Metaclass_GetBatteryState):
    from custom_msg_srv.srv._get_battery_state import GetBatteryState_Request as Request
    from custom_msg_srv.srv._get_battery_state import GetBatteryState_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
