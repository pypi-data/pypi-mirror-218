from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
app = FastAPI()
html = '\n<!DOCTYPE html>\n<html>\n    <head>\n        <title>Chat</title>\n    </head>\n    <body>\n        <h1>WebSocket Chat</h1>\n        <form action="" onsubmit="sendMessage(event)">\n            <input type="text" id="messageText" autocomplete="off"/>\n            <button>Send</button>\n        </form>\n        <ul id=\'messages\'>\n        </ul>\n        <script>\n            var ws = new WebSocket("ws://localhost:8000/ws");\n            ws.onmessage = function(event) {\n                var messages = document.getElementById(\'messages\')\n                var message = document.createElement(\'li\')\n                var content = document.createTextNode(event.data)\n                message.appendChild(content)\n                messages.appendChild(message)\n            };\n            function sendMessage(event) {\n                var input = document.getElementById("messageText")\n                ws.send(input.value)\n                input.value = \'\'\n                event.preventDefault()\n            }\n        </script>\n    </body>\n</html>\n'

@app.get('/')
async def get():
    return HTMLResponse(html)

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')