from server.conference.constants import MemberRole
from server.conference.types import MemberID, ConferenceID
from server.conference.canvas import Canvas


class ConferenceMember:
    role: MemberRole
    id: MemberID
    conference_id: ConferenceID
    canvas: Canvas | None = None

    def __init__(
        self,
        id: MemberID,
        conference_id: ConferenceID,
        role: MemberRole = MemberRole.PARTICIPANT,
    ) -> None:
        self.role = role
        self.id = id
        self.conference_id = conference_id

    def set_canvas(self, canvas: Canvas):
        self.canvas = canvas


class ConferenceMembers:
    _collection: dict[MemberID, ConferenceMember]

    def __init__(self) -> None:
        self._collection = {}

    def get_member(self, id: MemberID):
        return self._collection[id]

    def add_member(self, member: ConferenceMember):
        self._collection[member.id] = member
        return member

    def remove_member(self, id: MemberID):
        del self._collection[id]

    def get_all_members(self):
        return list(self._collection.values())

    def iter_all_members(self, *, exclude: list[ConferenceMember] = None):
        if exclude is None:
            for member in self._collection.values():
                yield member
            return
        for member in self._collection.values():
            if member not in exclude:
                yield member

    @property
    def is_empty(self):
        return bool(self._collection)
