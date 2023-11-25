from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from server.conference.conference_session import ConferenceSession
from server.config import INNER_PORT

router = APIRouter()

ws_debug_test_page = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = 179
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8179/ws/conference/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

canvases: dict[int, ConferenceSession] = {}


@router.get("/conference/{conference_id}")
async def get():
    return HTMLResponse(ws_debug_test_page)


@router.websocket("/ws/conference/{conference_id}")
async def websocket_endpoint(conference_id: int, websocket: WebSocket):
    # TODO: Validate access
    if conference_id not in canvases:
        canvases[conference_id] = ConferenceSession(conference_id)
    user = await canvases[conference_id].connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await canvases[conference_id].handle_action(user, data)
    except WebSocketDisconnect:
        canvases[conference_id].disconnect(websocket)
