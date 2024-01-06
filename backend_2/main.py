from typing import Union

from fastapi.responses import JSONResponse
from fw import Fw
from fastapi import FastAPI, Request, status
from endpoints import Endpoints

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

app = FastAPI()
fw = Fw()
endpoints = Endpoints(fw)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )



app.mount("/endpoints", endpoints.sub_app)

@app.get('/')
def home():
    return {"Hello": "World"}
