import pygame, math
from support import centred_text_at, rectangle_collision

class Generator_Ui:
    def __init__(self, window_data, ds, font, item_images):
        self.window_data = window_data
        self.ds = ds
        self.font = font

        # 1 = Main, 2 = Scroll window
        self.state = 1
        self.current_item = 1

        self.midpoint = [self.window_data["Width"] * 0.5, self.window_data["Height"] * 0.5]
        self.gui_size = 128
        self.half_size = self.gui_size * 0.5

        # Secondary stuff
        self.square_size = 32
        self.start_x = self.midpoint[0] - (self.square_size + 24)
        self.start_y = self.midpoint[1] - self.half_size + 8
        self.difference = self.square_size + 8 # Distance between TL of squares (32 = size, 8 is the margin)

        self.rect = (self.midpoint[0] - self.half_size, self.midpoint[1] - self.half_size, self.gui_size, self.gui_size)
        self.current_item_rect = (self.midpoint[0] - 16, self.midpoint[1] - 16, 32, 32)

        self.generatable_tiles = [1, 2]
        self.item_images = self.sort_images(item_images)
        self.open_tile = None

    def sort_images(self, img_data):
        out = [] # Only gets generatable images
        for i in range(len(img_data)):
            if i in self.generatable_tiles:
                out.append(img_data[i])
        return out

    def render_primary(self):
        self.ds.blit(self.item_images[self.current_item - 1], self.current_item_rect)
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] - 20, self.midpoint[1] - 20, 40, 40), 4)
        # centred_text_at(self.ds, self.font, (self.midpoint[0], self.midpoint[1] + 8 + 6), "Placeholder")

    def render_secondary(self):
        for i in range(2):
            y_change = math.floor(i / 3)
            self.ds.blit(self.item_images[i], (self.start_x + ((i - (y_change * 3)) * self.difference), self.start_y + (y_change * self.difference)))

    def secondary_mouse_event(self, mouseX, mouseY):
        for i in range(2):
            y_change = math.floor(i / 3)
            if rectangle_collision((mouseX, mouseY, 1, 1), (self.start_x + ((i - (y_change * 3)) * self.difference), self.start_y + (y_change * self.difference), self.square_size, self.square_size)):
                self.current_item = self.generatable_tiles[i]
                self.open_tile.generating = self.current_item
                self.state = 1

    def render(self):
        # UI base
        pygame.draw.rect(self.ds, (180, 180, 180), self.rect)
        pygame.draw.rect(self.ds, (140, 140, 140), self.rect, 4)
        if self.state == 1:
            self.render_primary()
        elif self.state == 2:
            self.render_secondary()

    def mouse_event(self, mouseX, mouseY):
        if self.state == 1:
            if rectangle_collision((mouseX, mouseY, 1, 1), self.current_item_rect):
                if self.state == 1: # Main
                    self.state = 2
        elif self.state == 2:
            self.secondary_mouse_event(mouseX, mouseY)