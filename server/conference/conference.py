from __future__ import annotations

from datetime import datetime

from server.conference.constants import MemberRole
from server.conference.exceptions import ForbiddenConferenceActionError
from server.conference.types import MemberID, ConferenceID, CanvasID, CanvasData
from server.conference.member import ConferenceMember, ConferenceMembers
from server.conference.canvas import Canvas, Canvases


class Conference:
    canvases: Canvases
    members: ConferenceMembers
    owner: ConferenceMember | None
    last_activity: datetime
    id: ConferenceID
    _canvas_id_counter: CanvasID = 0
    _member_id_counter: MemberID = 0
    sync_canvas_and_member_ids: bool
    expiration_time_limit: int
    is_user_counter_frozen: bool

    def __init__(
        self,
        id: ConferenceID,
        *,
        sync_canvas_and_member_ids: bool = False,
        expiration_time_limit: int = 2 * 60 * 60,
    ):
        self.id = id
        self.canvases = Canvases()
        self.members = ConferenceMembers()
        self.owner = None
        self.sync_canvas_and_member_ids = sync_canvas_and_member_ids
        self.expiration_time_limit = expiration_time_limit
        self.is_user_counter_frozen = True
        self.poke()

    def _generate_new_canvas_id(self) -> CanvasID:
        self._canvas_id_counter += 1
        return self._canvas_id_counter - 1

    def _generate_new_member_id(self) -> MemberID:
        self._member_id_counter += 1
        return self._member_id_counter - 1

    def check_canvas_owning_right(self, member: ConferenceMember) -> bool:
        return member.role >= MemberRole.PARTICIPANT

    def poke(self):
        self.last_activity = datetime.utcnow()

    def create_canvas(self, owners_id: list[MemberID] | None = None, *, id: int = None):
        if owners_id is None:
            owners_id = []
        if id is None:
            id = self._generate_new_canvas_id()
        canvas = Canvas(
            id=self._generate_new_canvas_id(),
            owners_id=owners_id,
            conference_id=self.id,
        )
        self.canvases.add_canvas(canvas)
        return canvas

    def create_member(self, role: MemberRole = MemberRole.PARTICIPANT):
        self.is_user_counter_frozen = False
        member = ConferenceMember(
            self._generate_new_member_id(), conference_id=self.id, role=role
        )
        self.members.add_member(member)
        if self.check_canvas_owning_right(member):
            canvas = self.create_canvas(
                owners_id=[member.id],
                id=member.id if self.sync_canvas_and_member_ids else None,
            )
            member.set_canvas(canvas)
        return member

    def is_active(self, timestamp: datetime = None) -> bool:
        if timestamp is None:
            timestamp = datetime.utcnow()
        return (
            not ((not self.is_user_counter_frozen) and self.members.is_empty)
            and (timestamp - self.last_activity).total_seconds()
            < self.expiration_time_limit
        )

    def iter_canvas_viewers(
        self, canvas: Canvas, *, exclude: list[ConferenceMember] = None
    ):
        if exclude is None:
            exclude = []
        for member in self.members.iter_all_members():
            if canvas.check_view_permission(member) and member not in exclude:
                yield member

    def write_canvas(
        self,
        sender: ConferenceMember,
        canvas: Canvas,
        new_data: CanvasData,
        force: bool = False,
    ):
        if force or canvas.check_edit_permission(sender):
            canvas.set_data(new_data)
        else:
            raise ForbiddenConferenceActionError(
                f"Member {sender.id} has no access to Canvas {canvas.id}"
            )
