from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from server.conference.exceptions import (
    ForbiddenConferenceAction,
    ConferenceValidationError,
)

from server.conference.message_coding.base_message_coder import BaseMessageCoder
from server.conference.conference_session import ConferenceSession, ConferenceMember
from server.conference.constants import MemberRole
from server.conference.messages import (
    BaseConferenceMessage,
    BaseClientMessage,
    WriteCanvasMessage,
    FullCanvasMessage,
    MemberInfoMessage,
)


class ConferenceController:
    conference: ConferenceSession
    message_coding: BaseMessageCoder
    __user_ws_table: dict[int, WebSocket]
    is_owner_role_vacant: bool
    is_alive: bool

    def __init__(self, message_coding: BaseMessageCoder, conference: ConferenceSession):
        self.message_coding = message_coding
        self.__user_ws_table = {}
        self.is_owner_role_vacant = True
        self.is_alive = True
        self.conference = conference

    @property
    def conference_id(self):
        return self.conference.id

    async def broadcast_message(self, message: BaseConferenceMessage):
        encoded_message = self.message_coding.encode_message(message)
        for reciever in message.recievers:
            ws = self.get_connection(reciever.id)
            await ws.send_text(encoded_message)

    async def on_connect(self, ws: WebSocket) -> ConferenceMember:
        self.conference.poke()

        if self.is_owner_role_vacant:
            role = MemberRole.OWNER
        else:
            role = MemberRole.PARTICIPANT
        new_member = self.conference.create_member(role)
        if self.is_owner_role_vacant:
            new_member.canvas.set_visibility_role(MemberRole.LISTENER)
        self.is_owner_role_vacant = False

        self.add_connection(new_member.id, websocket=ws)

        welcoming_message = MemberInfoMessage(
            recievers=(new_member,),  # NOTE: May change to iter_all_members()
            conference=self.conference,
            member=new_member,
        )
        await self.broadcast_message(welcoming_message)

        for canvas in self.conference.iter_all_canvases():
            if canvas.check_view_permission(member=new_member):
                canvas_message = FullCanvasMessage(
                    recievers=(new_member,),
                    conference=self.conference,
                    target_canvas=canvas,
                )
                await self.broadcast_message(canvas_message)

        if self.conference.check_canvas_possession_right(new_member):
            my_canvas_message = FullCanvasMessage(
                recievers=self.conference.iter_all_members(exclude=[new_member]),
                conference=self.conference,
                target_canvas=new_member.canvas,
            )
            await self.broadcast_message(my_canvas_message)

        return new_member

    async def on_disconnect(self, member: ConferenceMember):
        self.conference.poke()
        self.remove_connection(member.id)
        if not not self.conference.is_active():
            self.is_alive = False

    async def on_message(self, message: BaseClientMessage):
        self.conference.poke()
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
                response_message = FullCanvasMessage(
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
        return self.__user_ws_table[user_id]

    def add_connection(self, user_id: int, websocket: WebSocket):
        self.__user_ws_table[user_id] = websocket

    def remove_connection(self, user_id: int):
        del self.__user_ws_table[user_id]

    async def close_connection(self, user_id: int):
        await self.__user_ws_table[user_id].close()

    def should_be_terminated(self, timestamp: datetime | None = None) -> bool:
        return not (self.is_alive and self.conference.is_active(timestamp))

    async def run_connection_loop(self, websocket: WebSocket):
        member = await self.on_connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                try:
                    message = self.message_coding.decode_message(
                        message_str=data, sender=member
                    )
                    await self.on_message(message)
                except ConferenceValidationError:
                    # Handle invalid data
                    continue
        except WebSocketDisconnect:
            await self.close_connection(member.id)
            self.remove_connection(member.id)
