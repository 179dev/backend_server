from fastapi import WebSocket
from server.config import CANVAS_WIDTH, CANVAS_HEIGHT

# TODO: Include authorization checks and deanonimize


class CanvasSession:
    canvas_id: int
    drawing: str
    connections: list[WebSocket]

    def __init__(self, canvas_id: int):
        self.canvas_id = canvas_id
        self.drawing = ""
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        await websocket.send_text(self.drawing)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_canvas_update(self, signal: str, sender: WebSocket):
        self.drawing = signal
        # TODO: Add merging
        await self.broadcast_update(exclude=[sender])

    async def broadcast_update(self, exclude: list[WebSocket]):
        for connection in self.connections:
            if connection in exclude:
                continue
            await connection.send_text(self.drawing)
