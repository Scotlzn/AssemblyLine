import pygame, math
from support import rectangle_collision

class Splitter_Ui:
    def __init__(self, window_data, ds, font, item_images):
        self.window_data = window_data
        self.ds = ds
        self.font = font
        self.item_images = item_images

        self.state = 1 # 1 = Primary, 2 = Secondary
        self.open_tile = None

        # ---------- UI ----------
        self.midpoint = [self.window_data["Width"] * 0.5, self.window_data["Height"] * 0.5]
        self.width, self.height = 64, 64
        self.half_width, self.half_height = self.width * 0.5, self.height * 0.5
        self.rect = (self.midpoint[0] - self.half_width, self.midpoint[1] - self.half_height, self.width, self.height)
        self.current_item_rect = (self.midpoint[0] - 8, self.midpoint[1] - 8, 16, 16)

        # ------- Submenu -------
        self.submenu_surface = pygame.surface.Surface((60, 60))
        self.submenu_midpoint = [60 * 0.5, 60 * 0.5]

        self.square_size = 16
        self.start_x = self.submenu_midpoint[0] - (self.square_size + 12)
        self.difference = self.square_size + 4 # Distance between TL of squares (16 = size, 4 is the margin)
        self.scroll = 0
        self.total_items = len(self.item_images)
        self.selected_tile = None

    def mouse_event(self, mouseX, mouseY):
        if self.state == 1:
            if rectangle_collision((mouseX, mouseY, 1, 1), self.current_item_rect):
                self.state = 2
        else:
            first_visible = math.floor((self.scroll + 2) / 20)
            start_y = self.submenu_midpoint[1] - self.half_height + 4 + (self.square_size + 4) * first_visible
            mouseX -= self.midpoint[0] - self.half_width
            mouseY -= self.midpoint[1] - self.half_height
            for i in range(self.number_of_squares(first_visible)):
                y_change = math.floor(i / 3)
                if rectangle_collision((mouseX, mouseY, 1, 1), (self.start_x + ((i - (y_change * 3)) * self.difference), start_y + (y_change * self.difference) - self.scroll, 16, 16)):
                    self.selected_tile = first_visible * 3 + i
                    self.open_tile.recipe = self.selected_tile
                    self.state = 1

    def scroll_submenu(self, direction):
        self.scroll += direction * 5
        y_change = math.floor((self.total_items - 1) / 3) + 1
        if self.scroll < 0 or self.total_items < 10:
            self.scroll = 0
        elif self.scroll > 2 + (self.square_size + 4) * (y_change - 3) - 2:
            self.scroll = 2 + (self.square_size + 4) * (y_change - 3) - 2
    
    def render_primary(self):
        self.ds.blit(self.item_images[self.selected_tile], self.current_item_rect)
        if self.selected_tile == 0:
            pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] - 9, self.midpoint[1] - 9, 18, 18), 2)
        else:
            pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] - 10, self.midpoint[1] - 10, 20, 20), 2)

    def number_of_squares(self, first_visible):
        n = 12
        if first_visible > math.floor(self.total_items / 3) - 4:
            n = 12 - (3 - (self.total_items % 3))
            if first_visible == math.floor(self.total_items / 3) - 2:
                n = 9 - (3 - (self.total_items % 3))
        return min(n, self.total_items)

    def render_secondary(self):
        first_visible = math.floor((self.scroll + 2) / 20)
        start_y = self.submenu_midpoint[1] - self.half_height + 4 + (self.square_size + 4) * first_visible
        self.submenu_surface.fill((180, 180, 180))
        for i in range(self.number_of_squares(first_visible)):
            y_change = math.floor(i / 3)
            self.submenu_surface.blit(self.item_images[i], (self.start_x + ((i - (y_change * 3)) * self.difference), start_y + (y_change * self.difference)))
            # pygame.draw.rect(self.submenu_surface, (255, 0, 0), (self.start_x + ((i - (y_change * 3)) * self.difference), start_y + (y_change * self.difference) - self.scroll, 16, 16))
        self.ds.blit(self.submenu_surface, (self.midpoint[0] - self.half_width + 2, self.midpoint[1] - self.half_height + 2, self.width, self.height))

    def render(self):
        pygame.draw.rect(self.ds, (180, 180, 180), self.rect)
        pygame.draw.rect(self.ds, (140, 140, 140), self.rect, 2)
        if self.state == 1:
            self.render_primary()
        else:
            self.render_secondary()