import pygame, math
from support import centred_text_at, rectangle_collision, load_json, add_suffix

class MachineUi:
    def __init__(self, window_data, ds, font, item_images, images):
        self.window_data = window_data
        self.ds = ds
        self.font = font
        self.item_images = item_images

        self.state = 1 # 1 = Primary, 2 = Secondary
        self.open_tile = None

        self.images = images

        # -------- DATA ---------
        self.wire_drawer = load_json('./Data/wiredrawer')
        self.furnace = load_json('./Data/furnace')
        self.compressor = load_json('./Data/compressor')
        self.press = load_json('./Data/hydraulicpress')

        self.loaded_data = None
        self.total_recipes = None
        self.selected_recipe = None

        # ------- GUI --------
        self.midpoint = self.midpoint = [self.window_data["Width"] * 0.5, self.window_data["Height"] * 0.5]
        self.width, self.height = 128, 128
        self.half_width, self.half_height = self.width * 0.5, self.height * 0.5
        self.square_size = 32

        # ------- SUBMENU --------
        self.submenu_surface = pygame.surface.Surface((self.width - 8, self.height - 8))
        self.submenu_midpoint = [(self.width - 8) * 0.5, (self.height - 8) * 0.5]
        self.margin = 12
        self.scroll = 0

    def render_primary(self):
        self.render_recipe()
        self.render_inventory()

    def mouse_event(self, mouseX, mouseY):
        if self.state == 1:
            # ------ Submenu trigger -----
            if rectangle_collision((mouseX, mouseY, 1, 1), (332, self.midpoint[1] - (self.half_height * 0.5) - 16, 32, 32)):
                self.state = 2
            # ------ Empty ------
            elif rectangle_collision((mouseX, mouseY, 1, 1), (self.midpoint[0] + self.half_width - 14, self.midpoint[1] + self.half_height - 14, 10, 10)):
                self.open_tile.inventory = {}
        else:
            first_visable = math.floor((self.scroll + 2) / 44)
            distance = (self.submenu_midpoint[1] - (self.half_height * 0.5) - 16) + (32 + 12) * first_visable
            mouseX -= self.midpoint[0] - self.half_width
            mouseY -= self.midpoint[1] - self.half_height
            for i in range(4):
                rect = [self.submenu_midpoint[0] + 6, distance + i * (32 + 12) - self.scroll, 32, 32]
                if rectangle_collision((mouseX, mouseY, 1, 1), rect):
                    tile = first_visable + i
                    self.selected_recipe = self.loaded_data[tile]
                    self.open_tile.recipe = self.selected_recipe
                    self.state = 1

    def render(self):
        pygame.draw.rect(self.ds, (180, 180, 180), (self.midpoint[0] - self.half_width, self.midpoint[1] - self.half_height, self.width, self.height))
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] - self.half_width, self.midpoint[1] - self.half_height, self.width, self.height), 4)
        if self.state == 1:
            self.render_primary()
        else:
            self.render_submenu()

    def scroll_submenu(self, direction):
        self.scroll += direction * 5
        if self.scroll < 0 or self.total_recipes < 3:
            self.scroll = 0
        elif self.scroll > 14 + (32 + 12) * (self.total_recipes - 3) + 6:
            self.scroll = 14 + (32 + 12) * (self.total_recipes - 3) + 6

    def render_submenu(self):
        first_visable = math.floor((self.scroll + 2) / 44)
        start_y = (self.submenu_midpoint[1] - (self.half_height * 0.5) - 16) + (self.square_size + self.margin) * first_visable

        self.submenu_surface.fill((180, 180, 180))
        for i in range(min(4, self.total_recipes)):
            recipe = self.loaded_data[first_visable + i]
            self.submenu_surface.blit(self.item_images[recipe["input"]["id"]], (self.submenu_midpoint[0] - 44, start_y + (i * (self.square_size + self.margin)) - self.scroll))
            self.submenu_surface.blit(self.item_images[recipe["output"]], (self.submenu_midpoint[0] + 12, start_y + (i * (self.square_size + self.margin)) - self.scroll))
            self.submenu_surface.blit(self.images[0], (self.submenu_midpoint[0] - 8, (start_y + 8) + (i * (self.square_size + self.margin)) - self.scroll))

            amount = recipe["input"]["amt"]
            if amount > 0:
                centred_text_at(self.submenu_surface, self.font, (self.submenu_midpoint[0] - 44 + self.square_size, start_y + (i * (self.square_size + self.margin) - self.scroll)), str(amount))

        self.ds.blit(self.submenu_surface, (self.midpoint[0] - self.half_width + 4, self.midpoint[1] - self.half_height + 4))
        

    def render_recipe(self):
        recipe = self.selected_recipe
        self.ds.blit(self.item_images[recipe["input"]["id"]], (self.midpoint[0] - 44, self.midpoint[1] - (self.half_height * 0.5) - 16))
        self.ds.blit(self.item_images[recipe["output"]], (self.midpoint[0] + 12, self.midpoint[1] - (self.half_height * 0.5) - 16))
        self.ds.blit(self.images[0], (self.midpoint[0] - 8, self.midpoint[1] - (self.half_height * 0.5) - 8))
        amt = recipe["input"]["amt"]
        if amt <= 0: return
        centred_text_at(self.ds, self.font, (self.midpoint[0] - 44 + self.square_size, self.midpoint[1] - (self.half_height * 0.5) - 16), str(amt))

    def render_inventory(self):
        n = min(2, len(self.open_tile.inventory))
        margin, offset = 24, 16
        total_width = n * self.square_size + (n - 1) * margin
        start_x = self.midpoint[0] - total_width // 2
        start_y = (self.midpoint[1] + self.half_height * 0.5) - self.square_size // 2 

        # Inventory
        inventory = self.open_tile.inventory
        inventory_ids = list(inventory.keys())

        for i in range(n): # Squares
            x = start_x + i * (self.square_size + margin)
            self.ds.blit(self.item_images[inventory_ids[i]], (x, start_y - offset))
            centred_text_at(self.ds, self.font, (x + (self.square_size * 0.5), start_y + self.square_size + 12 - offset), add_suffix(inventory[inventory_ids[i]]))

        # Empty button
        self.ds.blit(self.images[1], (self.midpoint[0] + self.half_width - 14, self.midpoint[1] + self.half_height - 14))
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] + self.half_width - 16, self.midpoint[1] + self.half_height - 16, 14, 14), 2)