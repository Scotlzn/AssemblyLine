import pygame, math
from support import centred_text_at, rectangle_collision

class Generator_Ui:
    def __init__(self, ds, font, item_images):
        self.ds = ds
        self.font = font

        # 1 = Main, 2 = Scroll window
        self.state = 1
        self.current_item = 1

        self.midpoint = 192 * 0.5
        self.gui_size = 64
        self.half_size = self.gui_size * 0.5

        # Secondary stuff
        self.square_size = 16
        self.start_x = self.midpoint - (self.square_size + 12)
        self.start_y = self.midpoint - self.half_size + 4
        self.difference = self.square_size + 4 # Distance between TL of squares (16 = size, 4 is the margin)

        self.rect = (self.midpoint - self.half_size, self.midpoint - self.half_size, self.gui_size, self.gui_size)
        self.current_item_rect = (self.midpoint - 8, self.midpoint - 8, 16, 16)

        self.generatable_tiles = [1, 2]
        self.item_images = self.scale_up_images(item_images)
        self.open_tile = None

    def scale_up_images(self, img_data):
        out = [] # Scales up images and only gets the generatable ones
        for i in range(len(img_data)):
            if (i + 1) in self.generatable_tiles:
                img = img_data[i + 1]
                out.append(pygame.transform.scale(img, (self.square_size, self.square_size)))
        return out

    def render_primary(self):
        self.ds.blit(self.item_images[self.current_item - 1], self.current_item_rect)
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint - 10, self.midpoint - 10, 20, 20), 2)
        centred_text_at(self.ds, self.font, (self.midpoint, self.midpoint + 8 + 6), "Placeholder")

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
        pygame.draw.rect(self.ds, (140, 140, 140), self.rect, 2)
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