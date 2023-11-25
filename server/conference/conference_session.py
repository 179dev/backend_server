from fastapi import WebSocket
from server.conference.canvas_store import CanvasStore
from server.conference.constants import MemberRole

# TODO: Include authorization checks and deanonimize


class ConferenceMember:
    ws: WebSocket
    canvas: str | None
    role: MemberRole

    def __init__(
        self, ws: WebSocket, role: MemberRole = MemberRole.PARTICIPANT
    ) -> None:
        self.ws = ws
        self.role = role
        self.canvas = "" if self.has_a_canvas() else None

    async def send_text(self, text):
        await self.ws.send_text(text)

    def can_edit_canvas(self, canvas: CanvasStore):
        return self.can_edit_other_canvases() or canvas == self.canvas

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
        self.canvases = []

    async def connect(self, websocket: WebSocket, role: MemberRole = MemberRole.OWNER):
        await websocket.accept()
        user = ConferenceMember(websocket, role=role)
        self.connections.append(user)
        self.canvases.append(user.canvas)
        # TODO: send full canvas information on connection
        return user

    def disconnect(self, connection: ConferenceMember):
        self.connections.remove(connection)
        self.canvases.remove(connection.canvas)

    async def handle_action(
        self, action: dict, actor: ConferenceMember, signal: str
    ) -> list[int]:
        if not actor.can_do_anything():
            return
        canvas = self.canvases[action.canvas_id]
        if actor.can_edit_canvas(canvas):
            await self.broadcast_update(action, exclude=(actor,))

    async def broadcast_update(self, exclude: tuple[ConferenceMember] = None):
        if exclude is None:
            exclude = set()
        for connection in self.connections:
            if connection in exclude:
                continue
            await connection.send_text()
