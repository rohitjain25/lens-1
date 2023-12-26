from .utility import Utility


class Common:
    __utility = None

    def __init__(self):
        pass

    @property
    def utility(self):
        if self.__utility is None:
            self.__utility = Utility()
        return self.__utility
