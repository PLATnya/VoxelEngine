LIMIT_CHUNK_SIZE = 16


class Chunk:
    def __init__(self):
        self.voxels = []

    def isFull(self):
        return self.size >= LIMIT_CHUNK_SIZE

    def addVoxel(self, voxel):
        self.voxels.append(voxel)

    def removeVoxel(self,voxel):
        self.voxels.remove(voxel)

    @property
    def size(self):
        return len(self.voxels)

