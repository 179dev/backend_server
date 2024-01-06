from __future__ import annotations

from typing import TYPE_CHECKING

from server.conference.constants import MemberRole
from server.conference.types import MemberID, CanvasID, ConferenceID, CanvasData

if TYPE_CHECKING:
    from server.conference.conference import ConferenceMember


class Canvas:
    id: CanvasID
    data: CanvasData
    owners_id: list[MemberID]
    conference_id: ConferenceID
    visibility_role: MemberRole
    edition_role: MemberRole

    def __init__(
        self,
        id: CanvasID,
        owners_id: list[MemberID],
        conference_id: ConferenceID,
        visibility_role: MemberRole = MemberRole.ASSISTANT,
        edition_role: MemberRole = MemberRole.ASSISTANT,
    ) -> None:
        self.data = CanvasData("")
        self.conference_id = conference_id
        self.owners_id = owners_id
        self.id = id
        self.visibility_role = visibility_role
        self.edition_role = edition_role

    def set_visibility_role(self, visibility_role: MemberRole):
        self.visibility_role = visibility_role

    def set_edition_role(self, edition_role: MemberRole):
        self.edition_role = edition_role

    def check_edit_permission(self, member: ConferenceMember):
        if member.role >= self.edition_role:
            return True
        if member.id in self.owners_id:
            return True
        return False

    def check_view_permission(self, member: ConferenceMember):
        if member.role >= self.visibility_role:
            return True
        if member.id in self.owners_id:
            return True
        return False

    def set_data(self, canvas_data: CanvasData):
        self.data = canvas_data

    def get_data(self):
        return self.data


class Canvases:
    _collection: dict[CanvasID, Canvas]

    def __init__(self) -> None:
        self._collection = {}

    def get_canvas(self, id: CanvasID):
        return self._collection[id]

    def add_canvas(self, canvas: Canvas):
        self._collection[canvas.id] = canvas
        return canvas

    def remove_canvas(self, id: CanvasID):
        del self._collection[id]

    def get_all_canvases(self):
        return list(self._collection.values())

    def iter_all_canvases(self, *, exclude: list[CanvasID] = None):
        if exclude is None:
            for canvas in self._collection.values():
                yield canvas
            return
        for canvas in self._collection.values():
            if canvas not in exclude:
                yield canvas

    @property
    def is_empty(self):
        return bool(self._collection)
