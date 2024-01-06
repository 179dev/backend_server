from typing import NewType, Self
from uuid import UUID, uuid4


class CanvasData(str):
    pass


MemberID = NewType("MemberID", int)
CanvasID = NewType("CanvasID", int)


class ConferenceID:
    uuid: UUID

    def __init__(self, id: UUID | str | None = None):
        match id:
            case UUID():
                self.uuid = id
            case str():
                self.uuid = UUID(id)
            case _:
                self.uuid = uuid4()

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return str(self.uuid)

    def __eq__(self, __value: Self) -> bool:
        return self.uuid == __value.uuid

    def __ne__(self, __value: Self) -> bool:
        return self.uuid != __value.uuid
