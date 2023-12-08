from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from server.conference.messages import *
from server.conference.conference import ConferenceMember

if TYPE_CHECKING:
    from server.conference.conference import Conference


class BaseMessageCoder(abc.ABC):
    @abc.abstractstaticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        ...

    @abc.abstractstaticmethod
    def decode_message(
        message_str: str,
        sender: ConferenceMember,
        conference: Conference,
    ) -> BaseClientMessage:
        ...
