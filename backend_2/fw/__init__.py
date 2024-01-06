from .database import Database
from .services import Services
from .common import Common


class Fw:
    __services = None
    __database = None
    __common = None

    @property
    def services(self):
        if self.__services is None:
            self.__services = Services(self.database, self.common)
        return self.__services

    @property
    def database(self):
        if self.__database is None:
            self.__database = Database(self.common)
        return self.__database

    @property
    def common(self):
        if self.__common is None:
            self.__common = Common()
        return self.__common
