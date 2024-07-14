import pygame
from support import generate_empty_map

class Map:
    def __init__(self, ds):
        self.ds = ds
        self.tiles = self.generate_empty()
        self.images = self.generate_images()

    def generate_images(self):
        out = {}
        directions = [0, -90, 180, 90] # D-L-U-R
        tiles = [
            pygame.image.load('./Assets/conveyor.png').convert(),
            pygame.image.load('./Assets/generator.png').convert(),
            pygame.image.load('./Assets/seller.png').convert(),
            pygame.image.load('./Assets/crafter.png').convert()
            ]
        for tile in range(len(tiles)):
            img = tiles[tile]
            for i, dir in enumerate(directions):
                new_img = pygame.transform.rotate(img, dir)
                out[(tile * 4) + i + 1] = new_img
        return out

    def generate_empty(self):
        return generate_empty_map(12)

    def render(self):
        for y in range(12):
            for x in range(12):
                tile = self.tiles[y][x]
                if tile != 0:
                    self.ds.blit(self.images[tile], (x * 8, y * 8, 8, 8))

    def update(self):
        self.render()