from Engine import ChunkManager, np, VOXEL_SIZE
from Actor import Actor
import Session
import Session


class Voxel:
    def __init__(self, color, actor=None, position=(0, 0, 0)):
        chunk_manager = Session.GameSession().chunk_manager
        self.isActive = True

        self.parent = None
        self.color = color
        # add voxel to chunk for rendering
        self.chunkRef = None
        if len(chunk_manager.chunks) == 0 or chunk_manager.chunks[-1].isFull():
            self.chunkRef = chunk_manager.createChunk()
            self.chunkRef.addVoxel(self)
        else:
            self.chunkRef = chunk_manager.chunks[-1]
            self.chunkRef.addVoxel(self)

            # add voxel to actor for transformations
        if (actor != None):
            actor.voxels.append(self)
            self.parent = actor
        self.SetPosition(*position)

    def SetPosition(self, gridX, gridY, gridZ):
        if Session.GameSession().matrix_field[gridX, gridY, gridZ] == None:
            Session.GameSession().matrix_field[gridX, gridY, gridZ] = self
        gridFactor = VOXEL_SIZE * 2
        x = gridX * gridFactor
        y = gridY * gridFactor
        z = gridZ * gridFactor
        if self.parent != None:
            self.localPosition = np.array([x, y, z])
            self.globalPosition = np.array(self.parent.worldPosition) + np.array(self.localPosition)
        else:
            self.localPosition = np.array([0, 0, 0])
            self.globalPosition = np.array([x, y, z])

    def DeleteFromChunk(self):
        self.chunkRef.removeVoxel(self)

    def __del__(self):
        print("deleting voxel")
