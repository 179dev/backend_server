import abc

from server.conference.messages import *
from server.conference.conference_session import ConferenceMember
from server.conference.conference_manager import ConferenceManager


class BaseMessageCoder(abc.ABC):
    @abc.abstractstaticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        ...

    @abc.abstractstaticmethod
    def decode_message(
        message_str: str,
        sender: ConferenceMember,
        conference_manager: ConferenceManager,
    ) -> BaseClientMessage:
        ...
