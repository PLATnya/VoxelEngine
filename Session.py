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
        self.matrix_field = MatrixField()
        self.state = GameSessionState.PRELIFE

        GraphicSetup()
        self.events_handler = EventHandler()
        self.pressed_buffer = []

        self.chunk_manager = ChunkManager()
        self.actor_manager = ActorManager()
        from Voxel import Voxel
        self.construct_voxel = Voxel((0, 1, 0))
        self.ChangeState(GameSessionState.LIFE)

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

    def ChangeState(self, new_state):
        #TODO:changing states
        if new_state == GameSessionState.LIFE:
            self.construct_voxel.isActive = False
            self.matrix_field.SaveBuff()

            # start main life looop
        elif new_state == GameSessionState.PRELIFE:
            self.construct_voxel.isActive = True
            # if have buuf update matrix by buf else create matrix orclear it
            #activate construct voxel
            pass
        elif new_state == GameSessionState.AFTERLIFE:
            #do not create construct voxel
            #add restart button or event
            # gofuck yourself
            pass
        self.state = new_state

class MatrixField:
    def __init__(self):
        self.matrix = np.empty((MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE,2))
        self.matrix[:,:,:,0] = None
        self.matrix[:,:,:,1] = 0
        self.buff = np.array([],dtype = np.object0)

    def __getitem__(self, item):
        return self.matrix[item]

    def SaveBuff(self):
        pass

    def IsEmpty(self):
        pass



