from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, Response

from server.conference.conference_session import ConferenceSession
from server.conference.action import Action

from uuid import uuid4, UUID

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
