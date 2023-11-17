from fastapi import WebSocket
from server.canvas.canvas_store import CanvasStore

# TODO: Include authorization checks and deanonimize


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
        self.connections.append(websocket)
        # TODO: send full canvas information on connection

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_action(self, signal: str):
        # TODO: Decode signal and apply changes
        # to canvas store
        await self.broadcast_update()

    async def broadcast_update(self):
        for connection in self.connections:
            # TODO: actually broadcast update
            ...
