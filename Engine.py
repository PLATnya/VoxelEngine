import sys

from GraphicsEngine import *

from Chunk import Chunk

CAMERA_MOVEMENT_SPEED = 0.5

CAMERA_ROTATION_SPEED = 0.002


class ChunkManager:
    def __init__(self):
        self.chunks = []

    def createChunk(self):
        chunk = Chunk()
        self.chunks.append(chunk)
        return chunk

    def renderAll(self):
        for chunk in self.chunks:
            renderChunk(chunk)


class ActorManager:
    def __init__(self):
        self.actors = []

    def addActor(self, actor):
        self.actors.append(actor)


class Event:
    def __init__(self):
        self.onPygamEvent = False


class EventNoPygame(Event):
    def __init__(self):
        self.onPygamEvent = False

    def onNotify(self):
        pass


class EventOnPygame(Event):

    def __init__(self, event_type):
        self.event_type = event_type
        self.onPygamEvent = True

    def action(self):
        pass

    def onNotify(self, event):
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


class KeyDownEvent(EventOnPygame):
    def __init__(self, pressed_buffer):
        super().__init__(pg.KEYDOWN)
        self.pressed_buffer = pressed_buffer

    def action(self):
        self.key = self.event.key
        self.pressed_buffer.append(self.key)
    # EventHandler.addPressedInBuffer(self.key)
    # if (self.key == pg.K_LEFT):
    #
    #     glTranslatef(-0.1, 0, 0)
    # elif (self.key == pg.K_RIGHT):
    #     glTranslate(0.1, 0, 0)


class KeyUpEvent(EventOnPygame):
    def __init__(self, pressed_buffer):
        super().__init__(pg.KEYUP)
        self.pressed_buffer = pressed_buffer

    def action(self):
        self.key = self.event.key
        self.pressed_buffer.remove(self.key)


class CameraMoveEvent(EventNoPygame):
    def __init__(self, pressed_buffer):
        super().__init__()
        self.pressed_buffer = pressed_buffer

    def onNotify(self):
        if pg.K_d in self.pressed_buffer:
            main_camera.MoveRight(CAMERA_MOVEMENT_SPEED)
        if pg.K_a in self.pressed_buffer:
            main_camera.MoveRight(-CAMERA_MOVEMENT_SPEED)
        if pg.K_w in self.pressed_buffer:
            main_camera.MoveForward(CAMERA_MOVEMENT_SPEED)
        if pg.K_s in self.pressed_buffer:
            main_camera.MoveForward(-CAMERA_MOVEMENT_SPEED)



class CameraRotateEvent(EventNoPygame):
    def __init__(self):
        super().__init__()

    def onNotify(self):
        mouse_velocity = np.flip(np.array(pg.mouse.get_rel()) * CAMERA_ROTATION_SPEED)
        mouse_velocity[1] *= -1
        main_camera.Rotate(*mouse_velocity)

class EscapeButtonExitEvent(EventNoPygame):
    def __init__(self, pressed_buffer):
        super().__init__()
        self.pressed_buffer = pressed_buffer

    def onNotify(self):
        if pg.K_ESCAPE in self.pressed_buffer:
            exit()
            pg.quit()
            sys.exit()


class EventHandler:

    def __init__(self):
        self.eventsByPygame = []
        self.eventNoPygame = []

    def addEvent(self, event):
        if event.onPygamEvent:
            self.eventsByPygame.append(event)
        else:
            self.eventNoPygame.append(event)

    def addPressedInBuffer(self, key):
        self.pressed_buffer.append(key)

    def removePressedInBuffer(self, key):
        self.pressed_buffer.remove(key)

    def isPressed(self, key):
        return key in self.pressed_buffer

    def notifyByEvent(self, event_in):
        for event in self.eventsByPygame:
            event.onNotify(event_in)

    def notifyNoEvent(self):
        for event in self.eventNoPygame:
            event.onNotify()
