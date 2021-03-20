class Actor:
    def __init__(self):
        self.voxels = []
        self.startBehaviur = None
        self.endBehaviour = None
        self.tickBehaviour = None
        self.worldPosition = (0,0,0)
    def size(self):
        return len(self.voxels)

