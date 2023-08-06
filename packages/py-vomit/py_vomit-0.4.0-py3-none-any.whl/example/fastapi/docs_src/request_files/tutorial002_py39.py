from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.post('/files/')
async def create_files(files: list[bytes]=File()):
    return {'file_sizes': [len(file) for file in files]}

@app.post('/uploadfiles/')
async def create_upload_files(files: list[UploadFile]):
    return {'filenames': [file.filename for file in files]}

@app.get('/')
async def main():
    content = '\n<body>\n<form action="/files/" enctype="multipart/form-data" method="post">\n<input name="files" type="file" multiple>\n<input type="submit">\n</form>\n<form action="/uploadfiles/" enctype="multipart/form-data" method="post">\n<input name="files" type="file" multiple>\n<input type="submit">\n</form>\n</body>\n    '
    return HTMLResponse(content=content)