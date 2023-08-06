from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

def generate_html_response():
    html_content = '\n    <html>\n        <head>\n            <title>Some HTML in here</title>\n        </head>\n        <body>\n            <h1>Look ma! HTML!</h1>\n        </body>\n    </html>\n    '
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/items/', response_class=HTMLResponse)
async def read_items():
    return generate_html_response()