import pygame
from support import rectangle_collision
from UI.crafter_ui import Crafter_Ui
from UI.generator_ui import Generator_Ui

class Ui:
    def __init__(self, ds, game):
        self.ds = ds
        self.game = game
        self.font = pygame.font.Font('./Fonts/font.ttf', 10)

        self.crafter_ui = Crafter_Ui(self.ds, self.font)
        self.generator_ui = Generator_Ui(self.ds, self.font, self.game.item_images)

        self.active = {
            "crafter": False,
            "generator": False
        }

    def submenus(self, mouseX, mouseY):
        if self.active["generator"]:
            self.generator_ui.mouse_event(mouseX, mouseY)

    def update(self):
        if self.active["crafter"]:
            self.crafter_ui.render()
        elif self.active["generator"]:
            self.generator_ui.render()