from .database import Database
from .services import Services

class Fw:
    __services = None
    __database = None
    
    @property
    def services(self):
        if self.__services is None:
            self.__services = Services(self.database)
        return self.__services
    
    @property
    def database(self):
        if self.__database is None:
            self.__database = Database()
        return self.__database