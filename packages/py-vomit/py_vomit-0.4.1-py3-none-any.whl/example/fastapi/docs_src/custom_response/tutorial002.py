from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get('/items/', response_class=HTMLResponse)
async def read_items():
    return '\n    <html>\n        <head>\n            <title>Some HTML in here</title>\n        </head>\n        <body>\n            <h1>Look ma! HTML!</h1>\n        </body>\n    </html>\n    '