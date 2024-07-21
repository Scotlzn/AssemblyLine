import pygame
from support import generate_empty_map

class Map:
    def __init__(self, ds, tile_size):
        self.ds = ds
        self.width = 20
        self.height = 11
        self.tile_size = tile_size
        self.tiles = self.generate_empty()
        self.images = self.generate_images()

    def generate_images(self):
        out = {}
        directions = [0, -90, 180, 90] # D-L-U-R
        tiles = [
            pygame.image.load('./Assets/Tiles/conveyor.png').convert(),
            pygame.image.load('./Assets/Tiles/generator.png').convert(),
            pygame.image.load('./Assets/Tiles/seller.png').convert(),
            pygame.image.load('./Assets/Tiles/crafter.png').convert(),
            pygame.image.load('./Assets/Tiles/wiredrawer.png').convert(),
            pygame.image.load('./Assets/Tiles/selector2.png').convert(),
            pygame.image.load('./Assets/Tiles/selector3.png').convert(),
            pygame.image.load('./Assets/Tiles/splitter_l.png').convert(),
            pygame.image.load('./Assets/Tiles/splitter_r.png').convert(),
            pygame.image.load('./Assets/Tiles/tunnel_in.png').convert(),
            pygame.image.load('./Assets/Tiles/tunnel_out.png').convert()
            ]
        for tile in range(len(tiles)):
            img = tiles[tile]
            for i, dir in enumerate(directions):
                new_img = pygame.transform.rotate(img, dir)
                sized_img = pygame.transform.scale(new_img, (self.tile_size, self.tile_size))
                out[(tile * 4) + i + 1] = sized_img
        return out

    def generate_empty(self):
        return generate_empty_map(self.width, self.height)

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                if tile != 0:
                    self.ds.blit(tile.img, (tile.x, tile.y))

    def update(self):
        self.render()