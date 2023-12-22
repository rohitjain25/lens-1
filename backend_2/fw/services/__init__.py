from .authentication import Authentication

class Services:
    __authentication = None
    
    def __init__(self, database):
        self.__database = database
        pass
    
    @property
    def authentication(self):
        if self.__authentication is None:
            self.__authentication = Authentication()
        return self.__authentication