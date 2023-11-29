from fastapi import WebSocket
from server.conference.constants import MemberRole
from server.conference.action import Action
from server.config import CONFERENCE_EXPIRATION_TIME
from datetime import datetime
from uuid import UUID


class ConferenceMember:
    ws: WebSocket
    canvas: str | None
    role: MemberRole

    def __init__(
        self, ws: WebSocket, canvas_id: int, role: MemberRole = MemberRole.PARTICIPANT
    ) -> None:
        self.ws = ws
        self.role = role
        self.canvas = "" if self.has_canvas() else None
        self.canvas_id = canvas_id

    async def send_text(self, text: str):
        await self.ws.send_text(text)

    async def send_json(self, data: dict):
        await self.ws.send_json(data)

    def can_edit_canvas(self, canvas_id: int) -> bool:
        return self.can_edit_other_canvases() or (
            (canvas_id == self.canvas_id) and self.can_do_anything()
        )

    def can_edit_other_canvases(self) -> bool:
        return self.role >= MemberRole.ASSISTANT

    def has_canvas(self) -> bool:
        return self.role >= MemberRole.PARTICIPANT

    def can_do_anything(self) -> bool:
        return self.role >= MemberRole.PARTICIPANT


class ConferenceSession:
    connections: list[ConferenceMember]
    owner: ConferenceMember | None
    last_activity: datetime
    id: UUID

    def __init__(self, id: UUID):
        self.id = id
        self.connections = []
        self.owner = None
        self.poke()

    def poke(self):
        self.last_activity = datetime.utcnow()

    async def connect(
        self, websocket: WebSocket, role: MemberRole = MemberRole.PARTICIPANT
    ):
        await websocket.accept()

        if not self.connections:
            role = max(role, MemberRole.OWNER)

        user = ConferenceMember(websocket, len(self.connections), role)

        if not self.owner:
            self.owner = user

        self.connections.append(user)
        self.poke()

        await user.send_json(
            {"type": "welcome", "id": user.canvas_id, "role": user.role.value}
        )

        for other_user in self.connections:
            if other_user.has_canvas():
                await user.send_json(
                    Action(other_user.canvas_id, other_user.canvas).to_json()
                )

        await self.broadcast_update(
            Action(user.canvas_id, user.canvas), exclude=(user,)
        )

        return user

    def is_active(self, timestamp: datetime = None) -> bool:
        if timestamp is None:
            timestamp = datetime.utcnow()
        return (
            self.connections
            and (timestamp - self.last_activity).total_seconds()
            < CONFERENCE_EXPIRATION_TIME
        )

    def disconnect(self, connection: ConferenceMember):
        self.connections.remove(connection)

    async def handle_action(self, action: Action, actor: ConferenceMember):
        self.poke()

        if not actor.can_do_anything():
            return
        if not actor.can_edit_canvas(action.target_canvas_id):
            return

        try:
            self.connections[action.target_canvas_id].canvas = action.canvas_data
        except IndexError:
            return

        await self.broadcast_update(action, exclude=(actor,))

    async def broadcast_update(
        self, action: Action, exclude: tuple[ConferenceMember] = None
    ):
        if exclude is None:
            exclude = set()

        for connection in self.connections:
            if connection in exclude:
                continue
            await connection.send_json(action.to_json())
