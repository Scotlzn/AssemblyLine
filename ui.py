import pygame

class Ui:
    def __init__(self, ds, game):
        self.ds = ds
        self.game = game
        self.active = {
            "crafter": False
        }

    def render(self):
        if self.active["crafter"]:
            midpoint = 96 * 0.5
            pygame.draw.rect(self.ds, (180, 180, 180), (midpoint - 16, midpoint - 16, 32, 32))

    def update(self):
        self.render()