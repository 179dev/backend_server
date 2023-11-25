from fastapi import WebSocket
from server.conference.constants import MemberRole
from server.conference.action import Action


class ConferenceMember:
    ws: WebSocket
    canvas: str | None
    role: MemberRole

    def __init__(
        self, ws: WebSocket, canvas_id: int, role: MemberRole = MemberRole.PARTICIPANT
    ) -> None:
        self.ws = ws
        self.role = role
        self.canvas = "" if self.has_a_canvas() else None
        self.canvas_id = canvas_id

    async def send_text(self, text):
        await self.ws.send_text(text)

    async def send_json(self, json):
        await self.ws.send_json(json)

    def can_edit_canvas(self, canvas_id: int):
        return self.can_edit_other_canvases() or (
            (canvas_id == self.canvas_id) and self.can_do_anything()
        )

    def can_edit_other_canvases(self):
        return self.role >= MemberRole.ASSISTANT

    def has_a_canvas(self):
        return self.role >= MemberRole.PARTICIPANT

    def can_do_anything(self):
        return self.role >= MemberRole.PARTICIPANT


class ConferenceSession:
    conference_id: int
    connections: list[ConferenceMember]

    def __init__(self, conference_id: int):
        self.conference_id = conference_id
        self.connections = []

    async def connect(self, websocket: WebSocket, role: MemberRole = MemberRole.OWNER):
        await websocket.accept()
        user = ConferenceMember(websocket, len(self.connections), role)
        self.connections.append(user)
        await user.send_json({"type": "welcome", "id": user.canvas_id})
        for other_user in self.connections:
            if other_user.has_a_canvas():
                await user.send_json(
                    Action(other_user.canvas_id, other_user.canvas).to_json()
                )
        return user

    def disconnect(self, connection: ConferenceMember):
        self.connections.remove(connection)

    async def handle_action(self, action: Action, actor: ConferenceMember) -> list[int]:
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
