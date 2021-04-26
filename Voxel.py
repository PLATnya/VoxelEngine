from GraphicsEngine import np, VOXEL_SIZE
import Session


class Voxel:
    def __init__(self, color, actor=None, position=(0, 0, 0)):
        chunk_manager = Session.GameSession().chunk_manager
        self.isActive = True
        self.localPosition = None
        self.globalPosition = None
        self.parent = None
        self.color = color
        # add voxel to chunk for rendering
        self.chunkRef = None
        if len(chunk_manager.chunks) == 0 or chunk_manager.chunks[-1].is_full():
            self.chunkRef = chunk_manager.create_chunk()
            self.chunkRef.add_voxel(self)
        else:
            self.chunkRef = chunk_manager.chunks[-1]
            self.chunkRef.add_voxel(self)

            # add voxel to actor for transformations
        if actor is not None:
            actor.voxels.append(self)
            self.parent = actor
        self.set_position(*position)

    def set_position(self, grid_x, grid_y, grid_z):
        if Session.GameSession().matrix_field[grid_x, grid_y, grid_z, 0] is None:
            Session.GameSession().matrix_field[grid_x, grid_y, grid_z] = self
        grid_factor = VOXEL_SIZE * 2
        x = grid_x * grid_factor
        y = grid_y * grid_factor
        z = grid_z * grid_factor
        if self.parent is not None:
            self.localPosition = np.array([x, y, z])
            self.globalPosition = np.array(self.parent.worldPosition) + np.array(self.localPosition)
        else:
            self.localPosition = np.array([0, 0, 0])
            self.globalPosition = np.array([x, y, z])

    def delete_from_chunk(self):
        self.chunkRef.remove_voxel(self)

    def __del__(self):
        print("deleting voxel")
