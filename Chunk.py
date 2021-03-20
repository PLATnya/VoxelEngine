LIMIT_CHUNK_SIZE = 16

import numpy as np
class Chunk:
    def __init__(self):
        self.actors = []
    def addActor(self,actor):
        self.actors.append(actor)
    def size(self):
        return sum([actor.size() for actor in self.actors])

