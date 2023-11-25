from __future__ import annotations

from enum import Enum


class ActionStatusCode(Enum):
    SUCCESS = 0
    FAILURE = 1
    FORBIDDEN = 2

    def __str__(self):
        return str(self.value)


class MemberRole(Enum):
    OWNER = 4
    ASSISTANT = 3
    PARTICIPANT = 2
    LISTENER = 1

    def __lt__(self, __value: MemberRole) -> bool:
        return self.value < __value.value

    def __gt__(self, __value: MemberRole) -> bool:
        return self.value > __value.value

    def __le__(self, __value: MemberRole) -> bool:
        return self.value <= __value.value

    def __ge__(self, __value: MemberRole) -> bool:
        return self.value >= __value.value


class ActionTypeCodes:
    add_shape = 1
    remove_shape = 2
    add_handle = 3
    remove_handle = 4
    edit_shape_param = 5


class ShapeType(Enum):
    rectangle = 1
    ellipsis = 2
    circle = 3
    line = 4


DELIMITER_CHAR = ";"
RESPONSE_PREFIX = "#"
ACTION_BROADCAST_PREFIX = "!"
