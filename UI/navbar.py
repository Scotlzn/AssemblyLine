import pygame
from support import rectangle_collision, centred_text_at, add_suffix

class Navbar:
    def __init__(self, ds, game, font, tile_images):
        self.ds = ds
        self.game = game
        self.font = font
        self.tile_images = tile_images
        self.editor = game.editor

        self.build = pygame.image.load('./Assets/build.png').convert()
        self.build = pygame.transform.scale(self.build, (16, 16))

        # ------- TILES LAYOUT -------
        self.normal_tiles = [1, 2, 3, 4, 5, 6, 8, 10, 11, 13]
        self.extra_tiles = [1, 2, 3, 4, 5, 6, 7, 9, 12, 13]
        self.displayed_tiles = self.normal_tiles

        self.rect = (0, 192-16, 320, 16)

    def mouse_event(self, mouseX, mouseY):
        for i in range(1, len(self.displayed_tiles) + 1):
            if rectangle_collision((mouseX, mouseY, 1, 1), (i * 16 + (i * 1), 176, 16, 16)):
                self.editor.selected_tile = self.displayed_tiles[i - 1]

    def render(self):
        pygame.draw.rect(self.ds, '#333333', self.rect)
        self.ds.blit(self.build, (0, 176))
        for i in range(1, len(self.displayed_tiles) + 1):
            tile = self.tile_images[((self.displayed_tiles[i - 1] - 1) * 4) + 1]
            self.ds.blit(tile, (i * (16 + 1), 176))
        centred_text_at(self.ds, self.font, (230, 192-8), f'M/S: {add_suffix(self.game.mps)}')
        centred_text_at(self.ds, self.font, (290, 192-8), f'Money: {add_suffix(self.game.money)}')

    def update(self):
        self.render()