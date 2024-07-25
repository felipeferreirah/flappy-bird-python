from enum import IntEnum, auto


class Layer(IntEnum):
    BACKGROUND = auto()
    COIN = auto()
    OBSTACLE = auto()
    OBJECT = auto()
    FLOOR = auto()
    PLAYER = auto()
    UI = auto()
