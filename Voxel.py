class Voxel:
    def __init__(self, voxelSize):
        self.IsActive = false
        self.localPosition = (0,0,0)

        wireCube(voxelSize)
    def wireCube(voxelSize):
        cubeEdges = np.array(((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7)))

        for cubeEdge in cubeEdges:
            for cubeVertex in cubeEdge:
                glVertex3fv(cubeVertices[cubeVertex]*voxelSize)