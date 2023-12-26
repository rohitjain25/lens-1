from typing import Union
from fw import Fw
from fastapi import FastAPI
from endpoints import Endpoints

app = FastAPI()
fw = Fw()
endpoints = Endpoints(fw)


app.mount("/endpoints", endpoints.sub_app)

@app.get('/')
def home():
    return {"Hello": "World"}
