import pygame
from support import rectangle_collision, centred_text_at

class Navbar:
    def __init__(self, ds, game, font, tile_images):
        self.ds = ds
        self.game = game
        self.font = font
        self.tile_images = tile_images
        self.editor = game.editor

        self.rect = (0, 192-16, 320, 16)

    def mouse_event(self, mouseX, mouseY):
        for i in range(10):
            if rectangle_collision((mouseX, mouseY, 1, 1), (i * 16 + (i * 1), 176, 16, 16)):
                self.editor.selected_tile = i + 1

    def render(self):
        pygame.draw.rect(self.ds, '#333333', self.rect)
        for i in range(10):
            tile = self.tile_images[(i * 4) + 1]
            self.ds.blit(tile, (i * (16 + 1), 176))
        centred_text_at(self.ds, self.font, (230, 192-8), f'M/S: {self.game.mps}')
        centred_text_at(self.ds, self.font, (290, 192-8), f'Money: {self.game.money}')

    def update(self):
        self.render()