import drawsvg
import logging

import dataclasses
from enum import Enum
from fastapi import WebSocket
from server.config import CANVAS_WIDTH, CANVAS_HEIGHT

from server.canvas.canvas_action import Action

# TODO: Include authorization checks and deanonimize


class CanvasSession:
    canvas_id: int
    drawing: drawsvg.Drawing
    connections: list[WebSocket]

    def __init__(self, canvas_id: int):
        self.canvas_id = canvas_id
        self.drawing = drawsvg.Drawing(
            width=CANVAS_WIDTH, height=CANVAS_HEIGHT
        )
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        await websocket.send_text(self.drawing.as_svg())

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def handle_action(self, signal: str):
        logging.info(signal)
        print(signal)
        action = Action(signal)
        action.perform(self.drawing)
        # rect = drawsvg.Rectangle(0, 0, 100, 100)

        # self.drawing.append(rect)
        await self.broadcast_update()

    async def broadcast_update(self):
        for connection in self.connections:
            await connection.send_text(self.drawing.as_svg())
