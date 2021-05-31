from GraphicsEngine import np, VOXEL_SIZE
import Session


class Voxel:
    def __init__(self, color, actor=None, position=(0, 0), is_indexed_by_matrix=True):
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
        self.grid_position = None
        self.set_position(*position, is_indexed_by_matrix)


    def set_position(self, grid_x, grid_y, is_indexed_by_matrix):
        self.grid_position = np.array([grid_x, grid_y])
        is_can_be_places = True

        if is_indexed_by_matrix:
            if Session.GameSession().matrix_field[grid_x, grid_y, 0] is None:
                Session.GameSession().matrix_field[grid_x, grid_y, 0] = self
                is_can_be_places = True

        if is_can_be_places:
            grid_factor = VOXEL_SIZE * 2
            x = grid_x * grid_factor
            y = grid_y * grid_factor
            if self.parent is not None:
                self.localPosition = np.array([x, y])
                self.globalPosition = np.array(self.parent.worldPosition) + np.array(self.localPosition)
            else:
                self.localPosition = np.array([0, 0])
                self.globalPosition = np.array([x, y])

    def delete_from_chunk(self):
        self.chunkRef.remove_voxel(self)

    def __del__(self):
        print("deleting voxel")
