from __future__ import annotations

from server.conference.constants import MemberRole
from server.config import (
    CONFERENCE_EXPIRATION_TIME,
    CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS,
)
from server.conference.canvas import Canvas, CanvasData
from server.conference.exceptions import ForbiddenConferenceAction
from datetime import datetime
from uuid import UUID


class ConferenceMember:
    role: MemberRole
    id: int
    conference: ConferenceSession
    canvas: Canvas | None = None

    def __init__(
        self,
        id: int,
        conference: ConferenceSession,
        role: MemberRole = MemberRole.PARTICIPANT,
    ) -> None:
        self.role = role
        self.id = id
        self.conference = conference

    def set_canvas(self, canvas: Canvas):
        self.canvas = canvas


class ConferenceSession:
    canvases: dict[int, Canvas]
    members: dict[int, ConferenceMember]
    owner: ConferenceMember | None
    last_activity: datetime
    id: UUID
    _canvas_id_counter: int = 0
    _member_id_counter: int = 0
    sync_canvas_and_member_ids: bool

    def __init__(self, id: UUID):
        self.id = id
        self.canvases = []
        self.members = []
        self.owner = None
        self.sync_canvas_and_member_ids = CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS
        self.poke()

    def _generate_new_canvas_id(self):
        self._canvas_id_counter += 1
        return self._canvas_id_counter - 1

    def _generate_new_member_id(self):
        self._member_id_counter += 1
        return self._member_id_counter - 1

    def check_canvas_possession_right(self, member: ConferenceMember) -> bool:
        if member.role >= MemberRole.PARTICIPANT:
            return True
        return False

    def poke(self):
        self.last_activity = datetime.utcnow()

    def new_canvas(self, owners=None, *, id: int = None):
        if owners is None:
            owners = []
        if id is None:
            id = self._generate_new_canvas_id()
        canvas = Canvas(
            id=self._generate_new_canvas_id(),
            owners=owners,
            conference=self,
        )
        self.canvases[canvas.id] = canvas
        return canvas

    def new_member(self, role: MemberRole = MemberRole.PARTICIPANT):
        member = ConferenceMember(self._generate_new_member_id(), role, conference=self)
        self.members[member.id] = member
        if self.check_canvas_possession_right(member):
            canvas = self.new_canvas(
                [member], id=member.id if self.sync_canvas_and_member_ids else None
            )
            member.set_canvas(canvas)
        return member

    def get_member(self, id: int):
        return self.members[id]

    def get_canvas(self, id: int):
        return self.canvases[id]

    def is_active(self, timestamp: datetime = None) -> bool:
        if timestamp is None:
            timestamp = datetime.utcnow()
        return (
            self.members
            and (timestamp - self.last_activity).total_seconds()
            < CONFERENCE_EXPIRATION_TIME
        )

    def get_all_members(self):
        return list(self.members.values())

    def iter_canvas_viewers(self, canvas: Canvas):
        for member in self.iter_all_members():
            if canvas.check_view_permission(member):
                yield member

    def iter_all_members(self, *, exclude: list[ConferenceMember] = None):
        if exclude is None:
            return self.members.values()
        for member in self.members.values():
            if member not in exclude:
                yield member

    def iter_all_canvases(self, *, exclude: list[Canvas] = None):
        if exclude is None:
            return self.canvases.values()
        for canvas in self.canvases.values():
            if canvas not in exclude:
                yield canvas

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
            raise ForbiddenConferenceAction(
                f"Member {sender.id} has no access to Canvas {canvas.id}"
            )
