from fastapi import FastAPI
description = '\nChimichangApp API helps you do awesome stuff. 🚀\n\n## Items\n\nYou can **read items**.\n\n## Users\n\nYou will be able to:\n\n* **Create users** (_not implemented_).\n* **Read users** (_not implemented_).\n'
app = FastAPI(title='ChimichangApp', description=description, summary="Deadpool's favorite app. Nuff said.", version='0.0.1', terms_of_service='http://example.com/terms/', contact={'name': 'Deadpoolio the Amazing', 'url': 'http://x-force.example.com/contact/', 'email': 'dp@x-force.example.com'}, license_info={'name': 'Apache 2.0', 'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'})

@app.get('/items/')
async def read_items():
    return [{'name': 'Katana'}]