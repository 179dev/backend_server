import json

from server.conference.message_coding.base_message_coding import BaseMessageCoding
from server.conference.messages import *
from server.conference.conference_session import ConferenceMember


class JSONMessageCoding(BaseMessageCoding):
    @staticmethod
    def encode_message(message: BaseConferenceMessage) -> str:
        message_dict = {}
        match message:
            case SendFullCanvasMessage():
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
        message_dict = json.loads(message_str)
        match message_dict:
            case _:  # There is only one client message type yet
                message = WriteCanvasMessage(
                    sender=sender,
                    target_canvas=sender.conference.get_canvas(message_dict["target"]),
                    data_override=CanvasData(message_dict["drawing"]),
                )
                return message
