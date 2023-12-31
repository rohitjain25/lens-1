from enum import Enum

class Constants(object, metaclass=type):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError

# Classes derived from enums/Constants class

class WaitTime (int, Constants):
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


class Authorization_Level (str, Constants):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"
    LEVEL_5 = "level_5"

