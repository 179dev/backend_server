from uuid import uuid4

from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse, Response

from server.conference import main_conference_manager
from server.conference.exceptions import ConferenceNotFound


router = APIRouter()


@router.post("/conference/")
async def post():
    conference_controller = main_conference_manager.create_conference()
    return JSONResponse({"conference_id": str(conference_controller.conference_id)})


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(conference_id: str, websocket: WebSocket):
    try:
        conference_controller = main_conference_manager.get_conference(conference_id)
    except ConferenceNotFound:
        return Response("Conference does not exist", status_code=404)
    await websocket.accept()
    await conference_controller.run_connection_loop(websocket)
