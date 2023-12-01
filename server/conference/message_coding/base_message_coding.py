import abc

from server.conference.messages import *
from server.conference.conference_session import ConferenceMember


class BaseMessageCoding(abc.ABC):
    @abc.abstractstaticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        ...

    @abc.abstractstaticmethod
    def decode_message(message_str: str, sender: ConferenceMember) -> BaseClientMessage:
        ...
