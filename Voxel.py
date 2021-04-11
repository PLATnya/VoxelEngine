from Engine import ChunkManager,np,VOXEL_SIZE
from Actor import Actor
import Session
import Session
class Voxel:
    def __init__(self, color, actor = None):
        chunk_manager = Session.GameSession().chunk_manager
        self.IsActive = True
        self.localPosition = (0, 0, 0)
        self.globalPosition = (0,0,0)
        self.parent = None
        self.color = color
        # add voxel to chunk for rendering
        if len(chunk_manager.chunks) == 0 or chunk_manager.chunks[-1].isFull():
            chunk = chunk_manager.createChunk()
            chunk.addVoxel(self)
        else:
            chunk_manager.chunks[-1].addVoxel(self)

        # add voxel to actor for transformations
        if (actor != None):
            actor.voxels.append(self)
            self.parent = actor

            self.globalPosition = np.array(self.parent.worldPosition)

    def SetPosition(self, x,y,z):
        #TODO: grid position

        if self.parent!=None:
            self.localPosition = np.array([x,y,z])
            self.globalPosition = np.array(self.parent.worldPosition) + np.array(self.localPosition)
        else:
            self.globalPosition = np.array([x,y,z])