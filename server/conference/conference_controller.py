from fastapi import WebSocket

from server.conference.exceptions import ForbiddenConferenceAction

from server.conference.message_coding.base_message_coding import BaseMessageCoding
from server.conference.conference_session import ConferenceSession, ConferenceMember
from server.conference.constants import MemberRole
from server.conference.messages import (
    BaseConferenceMessage,
    WriteCanvasMessage,
    SendFullCanvasMessage,
    MemberInfoMessage,
)


class ConferenceController:
    conference: ConferenceSession
    message_coding: BaseMessageCoding
    _user_ws_table: dict[int, WebSocket]
    _is_owner_role_vacant: bool
    is_alive: bool

    def __init__(
        self, message_coding: BaseMessageCoding, conference: ConferenceSession
    ):
        self.message_coding = message_coding
        self._user_ws_table = {}
        self._is_owner_role_vacant = True
        self.is_alive = True
        self.conference = conference

    async def broadcast_message(self, message: BaseConferenceMessage):
        encoded_message = self.message_coding.encode_message(message)
        for reciever in message.recievers:
            ws = self.get_connection(reciever.id)
            await ws.send_text(encoded_message)

    async def on_connect(self, ws: WebSocket):
        self.conference.poke()
        if self._is_owner_role_vacant:
            role = MemberRole.OWNER
        else:
            role = MemberRole.PARTICIPANT
        self._is_owner_role_vacant = False
        new_member = self.conference.new_member(role)
        self.add_connection(new_member.id, websocket=ws)
        welcoming_message = MemberInfoMessage(
            recievers=(new_member,),  # NOTE: May change to iter_all_members()
            conference=self.conference,
            member=new_member,
        )
        await self.broadcast_message(welcoming_message)
        for canvas in self.conference.iter_all_canvases():
            if canvas.check_view_permission(member=new_member):
                canvas_message = SendFullCanvasMessage(
                    recievers=(new_member,),
                    conference=self.conference,
                    target_canvas=canvas,
                )
                await self.broadcast_message(canvas_message)
        if self.conference.check_canvas_possession_right(new_member):
            my_canvas_message = SendFullCanvasMessage(
                recievers=self.conference.iter_all_members(exclude=[new_member]),
                conference=self.conference,
                target_canvas=new_member.canvas,
            )
            await self.broadcast_message(my_canvas_message)

    async def on_disconnect(self, member: ConferenceMember):
        self.conference.poke()
        self.remove_connection(member.id)
        if not not self.conference.is_active():
            self.is_alive = False

    async def on_message(self, data: str, sender: ConferenceMember):
        self.conference.poke()
        message = self.message_coding.decode_message(data, sender=sender)
        match message:
            case WriteCanvasMessage():
                try:
                    self.conference.write_canvas(
                        sender=message.sender,
                        canvas=message.target_canvas,
                        new_data=message.data_override,
                    )
                except ForbiddenConferenceAction:
                    # Handle forbidden action
                    return
                response_message = SendFullCanvasMessage(
                    recievers=self.conference.iter_canvas_viewers(
                        message.target_canvas
                    ),
                    conference=self.conference,
                    target_canvas=message.target_canvas,
                )
                await self.broadcast_message(response_message)
            case _:
                pass

    def get_connection(self, user_id: int):
        return self._user_ws_table[user_id]

    def add_connection(self, user_id: int, websocket: WebSocket):
        self._user_ws_table[user_id] = websocket

    def remove_connection(self, user_id: int):
        self.close_connection(user_id)
        del self._user_ws_table[user_id]

    async def close_connection(self, user_id: int):
        await self._user_ws_table[user_id].close()
