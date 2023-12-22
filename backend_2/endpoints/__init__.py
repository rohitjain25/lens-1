from fastapi import FastAPI
from .authentication import Authentication

class Endpoints:
    def __init__(self, fw):
        self.__fw = fw
        self.__sections = {
            "/auth": Authentication
        }
        self.sub_app = FastAPI()
        self.__get_sections()
    
    def __get_sections(self):
        for section_name, section_class in self.__sections.items():
            section_class_obj = section_class(self.__fw)
            self.sub_app.mount(section_name, section_class_obj.sub_app)
            
        
        
    