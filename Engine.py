
import sys


from GraphicsEngine import *

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

class Event:
    def __init__(self, event_type):
        self.event_type = event_type
    def action(self):
        pass
    def onNotify(self, event):
        self.event = event
        if self.event_type == event.type:
            self.action()

class CloseEvent(Event):
    def __init__ (self):
        super().__init__(pg.QUIT)
    def action(self):
        exit()
        pg.quit()
        sys.exit()


class KeyDownEvent(Event):
    def __init__ (self):
        super().__init__(pg.KEYDOWN)
    def action(self):
        self.key = self.event.key
        if(self.key == pg.K_LEFT):
            glTranslatef(-0.1,0,0)
        elif(self.key == pg.K_RIGHT):
            glTranslate(0.1,0,0)



class EventHandler:
    def __init__ (self):
        self.events = []
    def notify(self,event_in):
        for event in self.events:
            event.onNotify(event_in)



