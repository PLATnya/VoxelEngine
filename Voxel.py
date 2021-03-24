from Engine import ChunkManager, Actor


class Voxel:
    def __init__(self, chunk_manager: ChunkManager, actor: Actor):
        self.IsActive = True
        self.localPosition = (0, 0, 0)

        # add voxel to chunk for rendering
        if chunk_manager.chunks[-1].isFull:
            chunk = chunk_manager.createChunk()
            chunk.addVoxel(self)
        else:
            chunk_manager.chunks[-1].append(self)

        # add voxel to actor for transformations
        actor.voxels.append(self)
