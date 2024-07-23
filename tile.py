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

        # ----- UNIQUE PROPERTIES -------
        self.generating = 1 # Only changes on generators
        self.split = 4 # For selectors

        # ----- MACHINE PROPERTIES ------
        self.inventory = {}
        self.recipe = None