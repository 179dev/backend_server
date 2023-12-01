from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from server.conference.conference_session import ConferenceMember, ConferenceSession

from server.conference.constants import MemberRole


class CanvasData(str):
    ...


class Canvas:
    data: CanvasData
    owners: list[ConferenceMember]
    conference: ConferenceSession
    id: int
    visibility_role: MemberRole
    edition_role: MemberRole

    def __init__(
        self,
        owners: list[ConferenceMember],
        conference: ConferenceSession,
        id: int,
        visibility_role: MemberRole = MemberRole.ASSISTANT,
        edition_role: MemberRole = MemberRole.ASSISTANT,
    ) -> None:
        self.data = CanvasData("")
        self.conference = conference
        self.owners = owners
        self.id = id
        self.visibility_role = visibility_role
        self.edition_role = edition_role

    def check_edit_permission(self, member: ConferenceMember):
        if member.role >= self.edition_role:
            return True
        if member in self.owners:
            return True
        return False

    def check_view_permission(self, member: ConferenceMember):
        if member.role >= self.visibility_role:
            return True
        if member in self.owners:
            return True
        return False

    def set_data(self, canvas_data: CanvasData):
        self.data = canvas_data

    def get_data(self):
        return self.data
