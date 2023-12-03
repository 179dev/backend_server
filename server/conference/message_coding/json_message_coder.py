import json

from server.conference.message_coding.base_message_coder import BaseMessageCoder
from server.conference.messages import *
from server.conference.conference_session import ConferenceMember
from server.conference.exceptions import ConferenceValidationError


class JSONMessageCoder(BaseMessageCoder):
    @staticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        message_dict = {}
        match message:
            case FullCanvasMessage():
                message_dict["type"] = "broadcast"
                message_dict["target"] = message.target_canvas.id
                message_dict["drawing"] = message.target_canvas.get_data()
            case MemberInfoMessage():
                message_dict["type"] = "welcome"
                message_dict["id"] = message.member.id
                message_dict["role"] = message.member.role.value
            case _:
                return NotImplemented
        return json.dumps(message_dict)

    @staticmethod
    def decode_message(message_str: str, sender: ConferenceMember) -> BaseClientMessage:
        try:
            message_dict = json.loads(message_str)
        except json.JSONDecodeError:
            raise ConferenceValidationError("Message is not JSON")
        match message_dict:
            case {"target": int(), "drawing": str()}:
                message = WriteCanvasMessage(
                    sender=sender,
                    target_canvas=sender.conference.get_canvas(message_dict["target"]),
                    data_override=CanvasData(message_dict["drawing"]),
                )
                return message
            case _:
                raise ConferenceValidationError("Unable to parse message")
