from __future__ import annotations

from typing import TYPE_CHECKING

from server.conference.constants import MemberRole
from server.conference.types import MemberID, CanvasID, ConferenceID

if TYPE_CHECKING:
    from server.conference.conference import ConferenceMember


class CanvasData(str):
    ...


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
