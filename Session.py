from enum import Enum
from Engine import *

MATRIX_SIZE = 100


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
    def InitSession(self):
        self.matrix = np.empty((MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE), dtype=np.object0)
        self.matrix.fill([None, 0])
        self.state = GameSessionState.PRELIFE

        GraphicSetup()
        self.events_handler = EventHandler()
        self.pressed_buffer = []

        self.chunk_manager = ChunkManager()
        self.actor_manager = ActorManager()
        from Voxel import Voxel
        self.construct_voxel = Voxel((0, 1, 0))

    def AddEvent(self, event):
        self.events_handler.addEvent(event)

    def MainLoop(self):
        while True:
            self.events_handler.notifyNoEvent()
            for event in pg.event.get():
                self.events_handler.notifyByEvent(event)

            clearScreen()
            self.chunk_manager.renderAll()
            pg.display.flip()
