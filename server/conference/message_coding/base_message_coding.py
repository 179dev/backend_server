from server.conference.messages import *
from server.conference.conference_session import ConferenceMember


class BaseMessageCoding:
    @staticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        ...

    @staticmethod
    def decode_message(message: str, sender: ConferenceMember) -> BaseClientMessage:
        ...
