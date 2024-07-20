import pygame
from support import rectangle_collision
from UI.navbar import Navbar
from UI.crafter_ui import Crafter_Ui
from UI.generator_ui import Generator_Ui

CRAFTER = 1
GENERATOR = 2

class Ui:
    def __init__(self, window_data, ds, game, item_images, recipes):
        self.ds = ds
        self.game = game
        self.font = pygame.font.Font('./Fonts/font.ttf', 10)
        self.images = self.scale_up_items(item_images)

        self.navbar = Navbar(self.ds, self.game, self.font, self.game.map.images)
        self.crafter_ui = Crafter_Ui(window_data, self.ds, self.font, self.images, recipes)
        self.generator_ui = Generator_Ui(window_data, self.ds, self.font, self.images)

        # 0 = None, 1 = Crafter, 2 = Generator
        self.active = 0

        self.midpoint = [window_data["Width"] * 0.5, window_data["Height"] * 0.5]
        self.ui_sizes= [[98, 60], [64, 64]]

    def scale_up_items(self, img_data):
        out = []
        for i in range(len(img_data)):
            img = img_data[i + 1]
            out.append(pygame.transform.scale(img, (16, 16)))
        return out

    def submenus(self, mouseX, mouseY):
        if self.active == GENERATOR:
            self.generator_ui.mouse_event(mouseX, mouseY)
        elif self.active == CRAFTER:
            self.crafter_ui.mouse_event(mouseX, mouseY)

    def close_ui(self, mouseX, mouseY):
        current_size = self.ui_sizes[self.active - 1]
        if not rectangle_collision((mouseX, mouseY, 1, 1), (self.midpoint[0] - (current_size[0]*0.5), self.midpoint[1] - (current_size[1]*0.5), current_size[0], current_size[1])):
            self.active = 0
        else:
            self.submenus(mouseX, mouseY)

    def scroll(self, direction, mouseX, mouseY):
        self.crafter_ui.scroll_submenu(direction)

    def mouse_event(self, tile, mouseX, mouseY):
        if self.active == 0:
            if tile != 0:
                if tile.tile == 2:
                    self.active = GENERATOR
                    self.generator_ui.open_tile = tile
                    self.generator_ui.current_item = tile.generating
                elif tile.tile == 4:
                    self.active = CRAFTER
                    self.crafter_ui.open_tile = tile
                    if tile.recipe != None:
                        self.crafter_ui.selected_recipe = tile.recipe
                    else:
                        self.crafter_ui.selected_recipe = self.crafter_ui.recipes[0]
            return

        self.close_ui(mouseX, mouseY)

    def update(self):
        self.navbar.update()
        if self.active == CRAFTER:
            self.crafter_ui.render()
        elif self.active == GENERATOR:
            self.generator_ui.render()