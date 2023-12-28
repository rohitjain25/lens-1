from typing import Annotated
from fastapi import FastAPI, Request, Response, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fw.common.constants import Authorization_Level
from fw.services.authentication.model import LoginForm, SignupForm, DeleteForm, SignupResponseModel


class Authentication:
    __sub_app = None

    def __init__(self, fw):
        self.__fw = fw

    @property
    def sub_app(self):
        if self.__sub_app is None:
            self.__sub_app = FastAPI()
            self.__get_endpoints()
        return self.__sub_app

    def __get_endpoints(self):
        @self.__sub_app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
            )
        @self.__sub_app.post("/signup")
        def signup(request: SignupForm, response:Response) -> SignupResponseModel:
            return self.__fw.services.authentication.signup(request, response)

        @self.__sub_app.post("/login")
        def login(request: LoginForm, response: Response):
            return self.__fw.services.authentication.login(request, response)

        @self.__sub_app.get("/user")
        def user(request=Depends(self.__fw.services.authentication.rbac[Authorization_Level.LEVEL_5])):
            return request

        @self.__sub_app.post("/delete")
        def delete(request: DeleteForm, response: Response, depends=Depends(self.__fw.services.authentication.rbac[Authorization_Level.LEVEL_1])):
            return self.__fw.services.authentication.delete(request, response)
