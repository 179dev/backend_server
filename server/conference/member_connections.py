from fastapi import WebSocket, WebSocketDisconnect
import abc

from server.conference.types import MemberID


class MemberConnectionClosed(Exception):
    pass


class BaseMemberConnection(abc.ABC):
    @abc.abstractmethod
    async def connect(self):
        ...

    @abc.abstractmethod
    async def send_text(self, text: str):
        ...

    @abc.abstractmethod
    async def receive_text(self) -> str:
        ...

    @abc.abstractmethod
    async def diconnect(self):
        ...


class WebsocketMemberConnection(BaseMemberConnection):
    websocket: WebSocket

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def connect(self):
        await self.websocket.accept()

    async def send_text(self, text: str):
        await self.websocket.send_text(text)

    async def receive_text(self) -> str:
        try:
            data = await self.websocket.receive_text()
        except WebSocketDisconnect as e:
            raise MemberConnectionClosed(e.reason)
        return data

    async def diconnect(self):
        await self.websocket.close()


class MemberConnectionsPool:
    __connections_table: dict[MemberID, BaseMemberConnection]

    def __init__(self) -> None:
        self.__connections_table = {}

    def get_connection(self, id: MemberID) -> BaseMemberConnection:
        return self.__connections_table[id] if id in self.__connections_table else None

    def add_connection(
        self, id: MemberID, connection: BaseMemberConnection
    ) -> BaseMemberConnection:
        self.__connections_table[id] = connection
        return connection

    def remove_connection(self, id: MemberID):
        del self.__connections_table[id]
