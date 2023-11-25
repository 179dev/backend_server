from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response

from server.vendor.repeat_every import repeat_every
from server.conference.conference_session import ConferenceSession
from server.conference.action import Action
from server.config import CONFERENCE_GC_RATE

from uuid import uuid4
import datetime

router = APIRouter()

conferences: dict[str, ConferenceSession] = {}


@router.post("/conference/")
async def post():
    new_id = str(uuid4())
    conferences[new_id] = ConferenceSession()
    return JSONResponse({"conference_id": new_id})


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(conference_id: str, websocket: WebSocket):
    if conference_id not in conferences:
        return Response("Conference does not exist", status_code=404)
    user = await conferences[conference_id].connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await conferences[conference_id].handle_action(Action.cook_data(data), user)
    except WebSocketDisconnect:
        conferences[conference_id].disconnect(user)
        if not conferences[conference_id].is_active():
            del conferences[conference_id]


@repeat_every(seconds=CONFERENCE_GC_RATE)
def conference_garbage_collect():
    for cid, conference in conferences.items():
        timestamp = datetime.datetime.utcnow()
        if not conference.is_active(timestamp):
            del conferences[cid]
