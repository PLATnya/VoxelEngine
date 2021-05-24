from enum import Enum
from GraphicsEngine import pg, clear_screen, graphic_setup
from Engine import EventHandler, ChunkManager, ActorManager
from Engine import PressEndEvent, PressStartEvent, PressRestartEvent
import numpy as np

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
            cls.matrix_field = MatrixField()
            cls.state = GameSessionState.PRELIFE

            graphic_setup()
            cls.events_handler = EventHandler()
            cls.pressed_buffer = []

            cls.chunk_manager = ChunkManager()
            cls.actor_manager = ActorManager()
            from Voxel import Voxel
            cls.construct_voxel = Voxel((0, 1, 0), is_indexed_by_matrix=False)
            cls.restart_event = PressRestartEvent()
            cls.start_event = PressStartEvent()
            cls.end_event = PressEndEvent()
        return cls._instances[cls]


class GameSession(metaclass=GameSessionMeta):
    def init_session(self):
        self.change_state(GameSessionState.PRELIFE)

    def add_event(self, event):
        self.events_handler.add_event(event)

    def main_loop(self):
        while True:
            self.events_handler.notify_no_event()
            for event in pg.event.get():
                self.events_handler.notify_by_event(event)
            clear_screen()
            self.chunk_manager.render_all()
            pg.display.flip()

    def change_state(self, new_state):
        if new_state == GameSessionState.PRELIFE:
            self.matrix_field.clear_instanced_buff()
            self.construct_voxel.isActive = True
            self.matrix_field.load_buff()
            self.events_handler.remove_event(self.restart_event)
            self.events_handler.add_event(self.start_event)

        elif new_state == GameSessionState.LIFE:
            self.construct_voxel.isActive = False
            self.matrix_field.save_buff()
            self.events_handler.remove_event(self.start_event)
            self.events_handler.add_event(self.end_event)
            # TODO: start main life looop

        elif new_state == GameSessionState.AFTERLIFE:
            self.construct_voxel.isActive = False
            # add restart button or event
            self.events_handler.add_event(self.restart_event)
            self.events_handler.remove_event(self.end_event)

        self.state = new_state
        print(self.state)


class MatrixField:
    def __init__(self):
        self.matrix = np.empty((MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE, 2), dtype=object)
        self.buff_indexes = np.array([])
        self.buff_instanced_indexes = []

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def save_buff(self):
        self.buff_indexes = np.argwhere(np.invert(self.matrix[:, :, :, 0] == None))

    def load_buff(self):
        if self.buff_indexes.size > 0:
            for n, index in enumerate(self.buff_indexes):
                from Voxel import Voxel
                self.matrix[index[0], index[1], index[2], 0] = Voxel((1, 0, 1), position=index)

    def is_empty(self):
        voxels_matrix = self.matrix[:, :, :, 0]
        return (np.sum(voxels_matrix == None) / np.size(voxels_matrix)) == 1.0

    def clear_instanced_buff(self):
        if len(self.buff_instanced_indexes) > 0:
            for n, index in enumerate(self.buff_instanced_indexes):
                from Voxel import Voxel
                self.matrix[index[0], index[1], index[2], 0].delete_from_chunk()
                self.matrix[index[0], index[1], index[2], 0] = None
        self.buff_instanced_indexes = []

        # # TODO: matrix delete voxels on restart
