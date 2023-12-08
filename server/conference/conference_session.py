from __future__ import annotations

from datetime import datetime
from uuid import UUID

from server.conference.constants import MemberRole
from server.config import (
    CONFERENCE_EXPIRATION_TIME,
    CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS,
)
from server.conference.canvas import Canvas, CanvasData
from server.conference.exceptions import ForbiddenConferenceActionError
from server.conference.types import MemberID, ConferenceID


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


class ConferenceSession:
    canvases: dict[int, Canvas]
    members: dict[MemberID, ConferenceMember]
    owner: ConferenceMember | None
    last_activity: datetime
    id: ConferenceID
    _canvas_id_counter: int = 0
    _member_id_counter: MemberID = 0
    sync_canvas_and_member_ids: bool

    def __init__(self, id: ConferenceID):
        self.id = id
        self.canvases = {}
        self.members = {}
        self.owner = None
        self.sync_canvas_and_member_ids = CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS
        self.poke()

    def _generate_new_canvas_id(self):
        self._canvas_id_counter += 1
        return self._canvas_id_counter - 1

    def _generate_new_member_id(self):
        self._member_id_counter += 1
        return self._member_id_counter - 1

    def check_canvas_owning_right(self, member: ConferenceMember) -> bool:
        return member.role >= MemberRole.PARTICIPANT

    def poke(self):
        self.last_activity = datetime.utcnow()

    def create_canvas(self, owners=None, *, id: int = None):
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

    def create_member(self, role: MemberRole = MemberRole.PARTICIPANT):
        member = ConferenceMember(
            self._generate_new_member_id(), conference_id=self.id, role=role
        )
        self.members[member.id] = member
        if self.check_canvas_owning_right(member):
            canvas = self.create_canvas(
                [member], id=member.id if self.sync_canvas_and_member_ids else None
            )
            member.set_canvas(canvas)
        return member

    def get_member(self, id: MemberID):
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
            for member in self.members.values():
                yield member
            return
        for member in self.members.values():
            if member not in exclude:
                yield member

    def iter_all_canvases(self, *, exclude: list[Canvas] = None):
        if exclude is None:
            for canvas in self.canvases.values():
                yield canvas
            return
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
            raise ForbiddenConferenceActionError(
                f"Member {sender.id} has no access to Canvas {canvas.id}"
            )
