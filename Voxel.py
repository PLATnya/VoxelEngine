from Engine import ChunkManager
from Actor import Actor


class Voxel:
    def __init__(self, chunk_manager: ChunkManager, actor: Actor):
        self.IsActive = True
        self.localPosition = (0, 0, 0)
        self.parent = None
        # add voxel to chunk for rendering
        if len(chunk_manager.chunks) == 0 or chunk_manager.chunks[-1].isFull():
            chunk = chunk_manager.createChunk()
            chunk.addVoxel(self)
        else:
            chunk_manager.chunks[-1].addVoxel(self)

        # add voxel to actor for transformations
        actor.voxels.append(self)
        self.parent = actor