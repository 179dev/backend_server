from fastapi import WebSocket
from server.canvas.canvas_store import CanvasStore
from server.canvas.actions.action_factory import ActionDecoder
from server.canvas.actions.actions import BaseAction

# TODO: Include authorization checks and deanonimize


class CanvasUser:
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


class CanvasSession:
    canvas_id: int
    canvas: CanvasStore
    connections: list[WebSocket]

    def __init__(self, canvas_id: int):
        self.canvas_id = canvas_id
        self.canvas = CanvasStore()
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user = CanvasUser(websocket)
        self.connections.append(user)
        # TODO: send full canvas information on connection
        return user

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_action(self, actor: CanvasUser, signal: str):
        action = ActionDecoder.decode(signal)
        actor.do(action).do(self.canvas)
        await self.broadcast_update(action)

    async def broadcast_update(self, action: BaseAction):
        for connection in self.connections:
            await connection.send_text(action.encode())
