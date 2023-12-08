from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import JSONResponse, Response

from server.conference.conferences_pool import ConferencesPool
from server.conference.exceptions import ConferenceNotFound
from server.conference.member_connections import WebsocketMemberConnection
from server.conference.types import ConferenceID

router = APIRouter()


def get_conferences_pool():
    from server.conference import main_conferences_pool

    return main_conferences_pool


@router.post("/create_conference/")
async def create_conference(
    conferences_pool: ConferencesPool = Depends(get_conferences_pool),
):
    global _id
    conference_controller = conferences_pool.create_conference()
    _id = conference_controller.conference_id
    return JSONResponse({"conference_id": str(conference_controller.conference_id)})


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(
    conference_id: str,
    websocket: WebSocket,
    conferences_pool: ConferencesPool = Depends(get_conferences_pool),
):
    connection = WebsocketMemberConnection(websocket)
    try:
        conference_controller = conferences_pool.get_conference(
            ConferenceID(conference_id)
        )
    except ConferenceNotFound:
        await connection.diconnect()
        return Response("Conference does not exist", status_code=404)
    await connection.connect()
    await conference_controller.run_connection_loop(connection)
