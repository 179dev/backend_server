import enum


class Permissions(enum.Enum):
    SELF = enum.auto()
    OTHER = enum.auto()
    ADMIN = enum.auto()
