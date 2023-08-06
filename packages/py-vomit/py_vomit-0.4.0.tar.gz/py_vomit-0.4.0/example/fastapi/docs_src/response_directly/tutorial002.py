from fastapi import FastAPI, Response
app = FastAPI()

@app.get('/legacy/')
def get_legacy_data():
    data = '<?xml version="1.0"?>\n    <shampoo>\n    <Header>\n        Apply shampoo here.\n    </Header>\n    <Body>\n        You\'ll have to use soap here.\n    </Body>\n    </shampoo>\n    '
    return Response(content=data, media_type='application/xml')