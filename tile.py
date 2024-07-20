import pygame

class Tile:
    def __init__(self, ds, pos, orientation, size, img):
        self.ds = ds

        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.img = img

        self.tile = orientation[0]
        self.rotation = orientation[1]

        self.generating = 1 # Only changes on generators

        self.inventory = {}
        self.recipe = None

    def render(self):
        self.ds.blit(self.img, (self.x, self.y))

    def update(self):
        self.render()