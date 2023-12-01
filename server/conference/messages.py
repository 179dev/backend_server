import dataclasses
from typing import Iterable

from server.conference.conference_session import ConferenceSession, ConferenceMember
from server.conference.canvas import Canvas, CanvasData


@dataclasses.dataclass
class BaseConferenceMessage:
    recievers: Iterable[ConferenceMember] | None
    conference: ConferenceSession


@dataclasses.dataclass
class SendFullCanvasMessage(BaseConferenceMessage):
    target_canvas: Canvas


@dataclasses.dataclass
class MemberInfoMessage(BaseConferenceMessage):
    member: ConferenceMember


@dataclasses.dataclass
class BaseClientMessage:
    sender: ConferenceMember


@dataclasses.dataclass
class WriteCanvasMessage(BaseClientMessage):
    target_canvas: Canvas
    data_override: CanvasData
