import sys

from GraphicsEngine import *

from Chunk import Chunk

CAMERA_MOVEMENT_SPEED = 0.3

CAMERA_ROTATION_SPEED = 0.002


class ChunkManager:
    def __init__(self):
        self.chunks = []

    def create_chunk(self):
        chunk = Chunk()
        self.chunks.append(chunk)
        return chunk

    def render_all(self):
        for chunk in self.chunks:
            render_chunk(chunk)


class ActorManager:
    def __init__(self):
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)


class Event:
    def __init__(self):
        self.onPygameEvent = False


class EventNoPygame(Event):
    def __init__(self):
        super().__init__()
        self.onPygameEvent = False

    def on_notify(self):
        pass


class EventOnPygame(Event):

    def __init__(self, event_type):
        super().__init__()
        self.event_type = event_type
        self.onPygameEvent = True
        self.event = None

    def action(self):
        pass

    def on_notify(self, event):
        self.event = event
        if self.event_type == event.type:
            self.action()


class CloseEvent(EventOnPygame):
    def __init__(self):
        super().__init__(pg.QUIT)

    def action(self):
        exit()
        pg.quit()
        sys.exit()


class KeyEvent(EventOnPygame):
    def __init__(self, pressed_buffer):
        super().__init__(pg.KEYDOWN)
        self.pressed_buffer = pressed_buffer
        self.key = None

    def action(self):
        self.key = self.event.key
        self.pressed_buffer.append(self.key)


class KeyUpEvent(EventOnPygame):
    def __init__(self, pressed_buffer):
        super().__init__(pg.KEYUP)
        self.pressed_buffer = pressed_buffer
        self.key = None

    def action(self):
        self.key = self.event.key
        self.pressed_buffer.remove(self.key)


class CameraMoveEvent(EventNoPygame):
    def __init__(self, pressed_buffer):
        super().__init__()
        self.pressed_buffer = pressed_buffer

    def on_notify(self):
        if pg.K_d in self.pressed_buffer:
            main_camera.move_right(CAMERA_MOVEMENT_SPEED)
        if pg.K_a in self.pressed_buffer:
            main_camera.move_right(-CAMERA_MOVEMENT_SPEED)
        if pg.K_w in self.pressed_buffer:
            main_camera.move_forward(CAMERA_MOVEMENT_SPEED)
        if pg.K_s in self.pressed_buffer:
            main_camera.move_forward(-CAMERA_MOVEMENT_SPEED)


class CameraRotateEvent(EventNoPygame):
    def __init__(self):
        super().__init__()

    def on_notify(self):
        mouse_velocity = np.flip(np.array(pg.mouse.get_rel()) * CAMERA_ROTATION_SPEED)
        mouse_velocity[1] *= -1
        main_camera.rotate(*mouse_velocity)


class EscapeButtonExitEvent(EventNoPygame):
    def __init__(self, pressed_buffer):
        super().__init__()
        self.pressed_buffer = pressed_buffer

    def on_notify(self):
        if pg.K_ESCAPE in self.pressed_buffer:
            exit()
            pg.quit()
            sys.exit()


class KeyDownEvent(EventNoPygame):
    pressed = False

    def __init__(self, pressed_buffer):
        super().__init__()
        self.key = None
        self.pressed_buffer = pressed_buffer

    def on_notify(self):
        if not self.pressed:
            if self.key in self.pressed_buffer:
                self.pressed = True
                return True
        else:
            if self.key not in self.pressed_buffer:
                self.pressed = False
        return False


class PressRestartEvent(KeyDownEvent):
    def __init__(self, pressed_buffer):
        super().__init__(pressed_buffer)
        self.key = pg.K_r

    def on_notify(self):
        if super(PressRestartEvent, self).on_notify():
            import Session
            Session.GameSession().change_state(Session.GameSessionState.PRELIFE)


class PressStartEvent(KeyDownEvent):
    def __init__(self, pressed_buffer):
        super().__init__(pressed_buffer)
        self.key = pg.K_SPACE

    def on_notify(self):
        if super(PressStartEvent, self).on_notify():
            import Session
            Session.GameSession().change_state(Session.GameSessionState.LIFE)


class PressEndEvent(KeyDownEvent):
    def __init__(self, pressed_buffer):
        super().__init__(pressed_buffer)
        self.key = pg.K_q

    def on_notify(self):
        if super(PressEndEvent, self).on_notify():
            import Session
            Session.GameSession().change_state(Session.GameSessionState.AFTERLIFE)


class EventHandler:

    def __init__(self):
        self.pressed_buffer = None
        self.eventsByPygame = []
        self.eventNoPygame = []

    def add_event(self, event):
        if event.onPygameEvent:
            self.eventsByPygame.append(event)
        else:
            self.eventNoPygame.append(event)

    def remove_event(self, event):
        if event in self.eventsByPygame:
            self.eventsByPygame.remove(event)
        elif event in self.eventNoPygame:
            self.eventNoPygame.remove(event)

    def add_pressed_in_buffer(self, key):
        self.pressed_buffer.append(key)

    def remove_pressed_in_buffer(self, key):
        self.pressed_buffer.remove(key)

    def is_pressed(self, key):
        return key in self.pressed_buffer

    def notify_by_event(self, event_in):
        for event in self.eventsByPygame:
            event.on_notify(event_in)

    def notify_no_event(self):
        for event in self.eventNoPygame:
            event.on_notify()
