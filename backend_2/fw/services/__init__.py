from .authentication import Authentication


class Services:
    __authentication = None

    def __init__(self, database, common_instance):
        self.__database = database
        self.__common_instance = common_instance
        pass

    @property
    def authentication(self):
        if self.__authentication is None:
            self.__authentication = Authentication(self.__database, self.__common_instance)
        return self.__authentication
