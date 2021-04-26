LIMIT_CHUNK_SIZE = 16


class Chunk:
    def __init__(self):
        self.voxels = []

    def is_full(self):
        return self.size >= LIMIT_CHUNK_SIZE

    def add_voxel(self, voxel):
        self.voxels.append(voxel)

    def remove_voxel(self, voxel):
        self.voxels.remove(voxel)

    @property
    def size(self):
        return len(self.voxels)

