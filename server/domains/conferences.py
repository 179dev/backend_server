from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse, Response

from server.conference import main_conference_manager
from server.conference.exceptions import ConferenceNotFound
from server.conference.member_connections import WebsocketMemberConnection
from server.conference.types import ConferenceID

router = APIRouter()


_id = None


@router.post("/conference/")
async def post():
    global _id
    conference_controller = main_conference_manager.create_conference()
    _id = conference_controller.conference_id
    return JSONResponse({"conference_id": str(conference_controller.conference_id)})


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(conference_id: str, websocket: WebSocket):
    connection = WebsocketMemberConnection(websocket)
    try:
        conference_controller = main_conference_manager.get_conference(
            ConferenceID(conference_id)
        )
    except ConferenceNotFound:
        raise Response("Conference does not exist", status_code=404)
    await connection.connect()
    await conference_controller.run_connection_loop(connection)
