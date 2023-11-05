import drawsvg
import dataclasses
from enum import Enum
from fastapi import WebSocket
from config import CANVAS_WIDTH, CANVAS_HEIGHT

# TODO: Include authorization checks and deanonimize


class ActionType(Enum):
    add_shape = 1
    remove_shape = 2
    add_handle = 3
    remove_handle = 4
    edit_shape_param = 5


@dataclasses.dataclass
class Action:
    type: ActionType
    args: list

    def __str__(self):
        return f"{self.type};{';'.join(self.args)}"


class CanvasSession:
    canvas_id: int
    drawing: drawsvg.Drawing
    connections: list[WebSocket]

    def __init__(self, canvas_id: int):
        self.canvas_id = canvas_id
        self.drawing = drawsvg.Drawing(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        websocket.send_text(self.drawing.as_svg())

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    def commit_action(self, action: Action):
        # TODO: Implement all actions
        if action.type == ActionType.add_shape:
            shape_type, x, y, w, h = action.args
            if shape_type == "rect":
                shape = drawsvg.Rectangle(int(x), int(y), int(w), int(h))
            else:
                shape = drawsvg.Ellipse(int(x), int(y), int(w), int(h))
            self.drawing.append(shape)

    def handle_action(self, string_action: str):
        action_type, *args = string_action.split(";")
        action = Action(action_type, args)
        self.commit_action(action)
        self.broadcast_update()

    async def broadcast_update(self):
        for connection in self.connections:
            await connection.send_text(self.drawing.as_svg())
