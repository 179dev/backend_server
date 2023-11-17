from enum import Enum


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
