import numpy as np
from enum import Enum


class GameSessionState(Enum):
    PRELIFE = -1
    LIFE = 0
    AFTERLIFE = 1


class GameSessionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GameSession(metaclass=GameSessionMeta):
    def __init__(self):
        self.matrix = np.array([])
        self.state = GameSessionState.PRELIFE