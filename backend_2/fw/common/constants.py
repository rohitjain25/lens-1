from enum import Enum


class WaitTime(Enum):
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


class Authorization_Level(Enum):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"
    LEVEL_5 = "level_5"