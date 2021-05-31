from enum import Enum
from GraphicsEngine import pg, clear_screen, graphic_setup, change_bg_color
from Engine import EventHandler, ChunkManager, ActorManager
from Engine import PressEndEvent, PressStartEvent, PressRestartEvent, MAKE_STEP_EVENT
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
            cls.step_delay_time = 1000

            graphic_setup()
            cls.events_handler = EventHandler()
            cls.pressed_buffer = []

            cls.chunk_manager = ChunkManager()
            cls.actor_manager = ActorManager()
            from Voxel import Voxel
            cls.construct_voxel = Voxel((0, 1, 0), position=np.array([MATRIX_SIZE/2, MATRIX_SIZE/2], dtype=np.int), is_indexed_by_matrix=False)
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

            if self.state == GameSessionState.LIFE:
                pass
            clear_screen()
            self.chunk_manager.render_all()
            pg.display.flip()

    def change_state(self, new_state):
        if new_state == GameSessionState.PRELIFE:
            change_bg_color((0,0,0,1))

            self.matrix_field.clear_instanced_buff()
            self.construct_voxel.isActive = True
            self.matrix_field.load_buff()
            self.events_handler.remove_event(self.restart_event)
            self.events_handler.add_event(self.start_event)

        elif new_state == GameSessionState.LIFE:
            change_bg_color((0.7, 0.3, 0.2, 1))
            self.matrix_field.save_buff()
            pg.time.set_timer(MAKE_STEP_EVENT, self.step_delay_time, -1)

            self.construct_voxel.isActive = False
            self.events_handler.remove_event(self.start_event)
            self.events_handler.add_event(self.end_event)

        elif new_state == GameSessionState.AFTERLIFE:
            change_bg_color((0.5, 0.5, 0.5, 1))
            pg.time.set_timer(MAKE_STEP_EVENT, 0)
            self.construct_voxel.isActive = False
            # add restart button or event
            self.events_handler.add_event(self.restart_event)
            self.events_handler.remove_event(self.end_event)
        self.state = new_state
        print(self.state)


class MatrixField:
    def __init__(self):
        self.matrix = np.empty((MATRIX_SIZE, MATRIX_SIZE, 2), dtype=object)
        self.matrix[:, :, 1] = 0
        self.buff_indexes = np.array([])
        self.buff_instanced_indexes = []

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def save_buff(self):
        self.buff_indexes = np.argwhere(np.invert(self.matrix[:, :, 0] == None))

    def load_buff(self):
        if self.buff_indexes.size > 0:
            for index in self.buff_indexes:
                from Voxel import Voxel
                self.matrix[index[0], index[1], 0] = Voxel((1, 0, 1), position=index)

    def is_empty(self):
        voxels_matrix = self.matrix[:, :, 0]
        return (np.sum(voxels_matrix == None) / np.size(voxels_matrix)) == 1.0

    def clear_instanced_buff(self):
        if len(self.buff_instanced_indexes) > 0:
            for index in self.buff_instanced_indexes:
                self.remove_instanced_voxel(index[0], index[1])
        self.buff_instanced_indexes = []

    def instance_voxel(self, x, y):
        from Voxel import Voxel
        self.matrix[x, y, 0] = Voxel((0, 0, 1), position=(x, y))
        self.buff_instanced_indexes.append([x, y])

    def remove_instanced_voxel(self, x, y):
        if self.matrix[x, y, 0] is not None:
            self.matrix[x, y, 0].delete_from_chunk()
            self.matrix[x, y, 0] = None

    def calc_neighbors(self, i, j):
        if self.matrix[i, j, 0] is not None:
            x = np.max([0, i - 1])
            matrix_limit = MATRIX_SIZE - 1
            while x <= np.min([i + 1, matrix_limit]):
                y = np.max([0, j - 1])
                while y <= np.min([j + 1, matrix_limit]):
                    if (x != i) or (y != j):
                        self.matrix[x,y, 1] += 1
                    y += 1
                x += 1

    def make_step(self):
        self.matrix[:, :, 1] = 0
        for x in range(MATRIX_SIZE):
            for y in range(MATRIX_SIZE):
                self.calc_neighbors(x, y)

        for x in range(MATRIX_SIZE):
            for y in range(MATRIX_SIZE):
                if self.matrix[x, y, 0] is None:
                    if self.matrix[x, y, 1] == 3:
                        self.instance_voxel(x, y)
                else:
                    if self.matrix[x, y, 1] > 3 or self.matrix[x, y, 1] < 2:
                        self.remove_instanced_voxel(x, y)