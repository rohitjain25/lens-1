from typing import Annotated
from fastapi import FastAPI, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fw.services.authentication.model import LoginForm, SignupForm


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
        @self.__sub_app.post("/signup")
        def signup(request: SignupForm) -> SignupForm:
            return self.__fw.services.authentication.signup(request)

        @self.__sub_app.post("/login")
        def login(request: LoginForm, response: Response):
            return self.__fw.services.authentication.login(request, response)

        @self.__sub_app.get("/user")
        def user(request=Depends(self.__fw.services.authentication.rbac["level_5"])):
            return request
