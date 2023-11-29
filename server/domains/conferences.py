from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response

from server.conference.conference_session import ConferenceSession
from server.conference.action import Action
from server.conference import main_conference_sessions_pool
from server.conference.exceptions import ConferenceNotFound


router = APIRouter()


@router.post("/conference/")
async def post():
    conference_session = main_conference_sessions_pool.create_conference_session()
    return JSONResponse({"conference_id": str(conference_session.id)})


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(conference_id: str, websocket: WebSocket):
    try:
        conference = main_conference_sessions_pool.get_conference_session(conference_id)
    except ConferenceNotFound:
        return Response("Conference does not exist", status_code=404)
    user = await conference.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await conference.handle_action(Action.from_raw_data(data), user)
    except WebSocketDisconnect:
        conference.disconnect(user)
        if not conference.is_active():
            main_conference_sessions_pool.terminate_conference_session(conference_id)
