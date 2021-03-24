class Actor:
    def __init__(self):
        self.voxels = []
        self.startBehaviour = None
        self.endBehaviour = None
        self.tickBehaviour = None
        self.worldPosition = (0, 0, 0)

    @property
    def size(self):
        return len(self.voxels)


