from typing import Union
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, WebSocketException, status
from fastapi.responses import HTMLResponse
app = FastAPI()
html = '\n<!DOCTYPE html>\n<html>\n    <head>\n        <title>Chat</title>\n    </head>\n    <body>\n        <h1>WebSocket Chat</h1>\n        <form action="" onsubmit="sendMessage(event)">\n            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>\n            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>\n            <button onclick="connect(event)">Connect</button>\n            <hr>\n            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>\n            <button>Send</button>\n        </form>\n        <ul id=\'messages\'>\n        </ul>\n        <script>\n        var ws = null;\n            function connect(event) {\n                var itemId = document.getElementById("itemId")\n                var token = document.getElementById("token")\n                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);\n                ws.onmessage = function(event) {\n                    var messages = document.getElementById(\'messages\')\n                    var message = document.createElement(\'li\')\n                    var content = document.createTextNode(event.data)\n                    message.appendChild(content)\n                    messages.appendChild(message)\n                };\n                event.preventDefault()\n            }\n            function sendMessage(event) {\n                var input = document.getElementById("messageText")\n                ws.send(input.value)\n                input.value = \'\'\n                event.preventDefault()\n            }\n        </script>\n    </body>\n</html>\n'

@app.get('/')
async def get():
    return HTMLResponse(html)

async def get_cookie_or_token(websocket: WebSocket, session: Union[str, None]=Cookie(default=None), token: Union[str, None]=Query(default=None)):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket('/items/{item_id}/ws')
async def websocket_endpoint(websocket: WebSocket, item_id: str, q: Union[int, None]=None, cookie_or_token: str=Depends(get_cookie_or_token)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Session cookie or query token value is: {cookie_or_token}')
        if q is not None:
            await websocket.send_text(f'Query parameter q is: {q}')
        await websocket.send_text(f'Message text was: {data}, for item ID: {item_id}')