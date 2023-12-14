from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from server.conference.conferences_pool import ConferencesPool

router = APIRouter()


def get_conferences_pool():
    from server.conference import main_conferences_pool

    return main_conferences_pool


router = APIRouter()

WS_DEBUG_TEST_PAGE = """
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
            var client_id = "$$CONFERENCE_ID"
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8179/ws/conference/$$CONFERENCE_ID`);
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


@router.get("/conference/{conference_id}")
async def get(conference_id: str):
    return HTMLResponse(WS_DEBUG_TEST_PAGE.replace("$$CONFERENCE_ID", conference_id))


@router.get("/conferences/")
async def conferences(
    conferences_pool: ConferencesPool = Depends(get_conferences_pool),
):
    ids = conferences_pool._conferences.keys()

    def item(id):
        return f'<a href="http://localhost:8179/conference/{id}">{id}</a>'

    return HTMLResponse("<br>".join(map(item, ids)))
