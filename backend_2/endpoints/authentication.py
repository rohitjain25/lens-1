from fastapi import FastAPI


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
        @self.__sub_app.get("/")
        def get_users():
            self.__fw.services
            return {'name': "Ronak Jain"}
    