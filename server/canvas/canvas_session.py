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
        """
        Sends the given text through the websocket connection.

        Args:
            text (str): The text to be sent through the websocket connection.

        Returns:
            None
        """
        await self.ws.send_text(text)

    def do(self, action: BaseAction) -> BaseAction:
        """
        Appends the given action to the history list and returns the action.

        Parameters:
            action (BaseAction): The action to be appended to the history list.

        Returns:
            BaseAction: The appended action.
        """
        if self.backwards_offset:
            self.history = self.history[: -self.backwards_offset]
            self.backwards_offset = 0
        self.history.append(action)
        return action

    def undo(self) -> BaseAction | None:
        """
        Undoes the previous action in the history of the object.

        Returns:
            BaseAction | None: The reversed action from the history, or None
            if there are no more actions to undo.
        """
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
        """
        Connects a websocket to the server.

        Parameters:
            websocket (WebSocket): The websocket to connect.

        Returns:
            CanvasUser: The user object representing the connected websocket.
        """
        await websocket.accept()
        user = CanvasUser(websocket)
        self.connections.append(user)
        # TODO: send full canvas information on connection
        return user

    def disconnect(self, websocket: WebSocket):
        """
        Remove the given WebSocket from the list of active connections.

        Parameters:
            websocket (WebSocket): The WebSocket to be disconnected.

        Returns:
            None
        """
        self.connections.remove(websocket)

    async def handle_action(self, actor: CanvasUser, signal: str):
        """
        Handles an action triggered by a CanvasUser.

        Args:
            actor (CanvasUser): The user who triggered the action.
            signal (str): The signal representing the action.

        Returns:
            None

        Raises:
            None
        """
        action = ActionDecoder.decode(signal)
        actor.do(action).do(self.canvas)
        await self.broadcast_update(action)

    async def broadcast_update(self, action: BaseAction):
        """
        Broadcasts an update to all connected clients.

        Args:
            action (BaseAction): The action to be broadcasted.

        Returns:
            None
        """
        for connection in self.connections:
            await connection.send_text(action.encode())
