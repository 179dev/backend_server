from __future__ import annotations

from enum import Enum


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
