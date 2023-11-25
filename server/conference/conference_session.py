from fastapi import WebSocket
from server.conference.canvas_store import CanvasStore
from server.conference.actions.action_factory import ActionDecoder
from server.conference.actions.actions import BaseAction

# TODO: Include authorization checks and deanonimize


class ConferenceMember:
    ws: WebSocket
    history: list[BaseAction]
    backwards_offset: int

    def __init__(self, ws: WebSocket) -> None:
        self.ws = ws
        self.history = []
        self.backwards_offset = 0

    async def send_text(self, text):
        await self.ws.send_text(text)

    def do(self, action: BaseAction) -> BaseAction:
        if self.backwards_offset:
            self.history = self.history[: -self.backwards_offset]
            self.backwards_offset = 0
        self.history.append(action)
        return action

    def undo(self) -> BaseAction | None:
        if self.backwards_offset >= len(self.history):
            self.backwards_offset = len(self.history)
            return
        self.backwards_offset += 1
        return self.history[-self.backwards_offset].reverse_action()


class ConferenceSession:
    conference_id: int
    canvas: CanvasStore
    connections: list[WebSocket]

    def __init__(self, conference_id: int):
        self.conference_id = conference_id
        self.canvas = CanvasStore()
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user = ConferenceMember(websocket)
        self.connections.append(user)
        # TODO: send full canvas information on connection
        return user

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_action(self, actor: ConferenceMember, signal: str):
        action = ActionDecoder.decode(signal)
        actor.do(action).do(self.canvas)
        await self.broadcast_update(action)

    async def broadcast_update(self, action: BaseAction):
        for connection in self.connections:
            await connection.send_text(action.encode())
