from server.conference.messages import *


class BaseMessageCoding:
    @staticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        ...

    @staticmethod
    def decode_message(message: str) -> BaseClientMessage:
        ...
