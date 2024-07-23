class Editor:
    def __init__(self):
        self.active = False

        # 1 = down, 2 = left, 3 = up, 4 = right
        self.rotation = 1
        self.selected_tile = 1

        self.more_tiles_toggle = False

        self.directions = {
            1: (0, 1),   # Down
            2: (-1, 0),  # Left
            3: (0, -1),   # Up
            4: (1, 0)   # Right
        }

    def get_correct_index(self):
        return ((self.selected_tile - 1) * 4 + self.rotation)

    def get_movement_from_rotation(self, rotation):
        return self.directions[rotation]

    def change_rotation(self, step):
        self.rotation += step
        if self.rotation == 4 + 1:
            self.rotation = 1
        elif self.rotation == 0:
            self.rotation = 4