from fastapi import WebSocket
from server.conference.canvas_store import CanvasStore
from server.conference.actions.action_encoding import ActionEncoding
from server.conference.actions.actions import BaseAction
from server.conference.constants import MemberRole, ActionStatusCode

# TODO: Include authorization checks and deanonimize


class ConferenceMember:
    ws: WebSocket
    history: list[BaseAction]
    backwards_offset: int
    canvas: CanvasStore | None
    role: MemberRole

    def __init__(
        self, ws: WebSocket, role: MemberRole = MemberRole.PARTICIPANT
    ) -> None:
        self.ws = ws
        self.role = role
        self.history = []
        self.backwards_offset = 0
        self.canvas = CanvasStore() if self.has_a_canvas() else None

    async def send_text(self, text):
        await self.ws.send_text(text)

    def record(self, action: BaseAction) -> BaseAction:
        if self.backwards_offset:
            self.history = self.history[: -self.backwards_offset]
            self.backwards_offset = 0
        self.history.append(action)
        return action

    def revert(self) -> BaseAction | None:
        if self.backwards_offset >= len(self.history):
            self.backwards_offset = len(self.history)
            return
        self.backwards_offset += 1
        return self.history[-self.backwards_offset].reverse_action()

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
    canvases: list[CanvasStore]
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

    async def handle_action(self, actor: ConferenceMember, signal: str) -> list[int]:
        if not actor.can_do_anything():
            return
        action, signal_id = ActionEncoding.decode(signal)
        canvas = self.canvases[action.canvas_id]
        if actor.can_edit_canvas(canvas):
            action.record(actor).do(canvas)
            await self.broadcast_update(action, exclude=(actor,))
            await actor.send_text(
                ActionEncoding.encode_action_response(
                    signal_id, ActionStatusCode.SUCCESS, action.response_data()
                )
            )
            return
        await actor.send_text(
            ActionEncoding.encode_action_response(
                signal_id, ActionStatusCode.FORBIDDEN, []
            )
        )

    async def broadcast_update(
        self, action: BaseAction, exclude: tuple[ConferenceMember] = None
    ):
        if exclude is None:
            exclude = set()
        for connection in self.connections:
            if connection in exclude:
                continue
            await connection.send_text(ActionEncoding.encode_action(action))
