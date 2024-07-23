import pygame, math
from support import centred_text_at, rectangle_collision

class Crafter_Ui:
    def __init__(self, window_data, ds, font, item_images, images, recipes):
        self.window_data = window_data
        self.ds = ds
        self.font = font
        self.item_images = item_images
        self.recipes = recipes
        self.open_tile = None

        self.state = 1 # 1 = Main, 2 = Submenu

        self.images = images
        none_img = pygame.image.load('./Assets/none.png').convert()
        none_img.set_colorkey((0, 0, 0))
        self.item_images.insert(0, none_img) # Insert none tile

        # -------- Window data -------
        self.midpoint = self.midpoint = [self.window_data["Width"] * 0.5, self.window_data["Height"] * 0.5]
        self.gui_width, self.gui_height = 98, 60
        self.half_width, self.half_height = self.gui_width * 0.5, self.gui_height * 0.5
        self.quarter = self.midpoint[1] + (self.half_height * 0.5)

        # ------- Recipe rendering --------
        self.number_of_squares = 4
        self.square_size, self.margin, self.offset = 16, 6, 3
        self.total_width = self.number_of_squares * self.square_size + (self.number_of_squares - 1) * self.margin

        # ------- Submenu -----------
        self.submenu_surface = pygame.surface.Surface((94, 56))
        self.submenu_midpoint = [94 * 0.5, 56 * 0.5]
        self.scroll = 0
        self.total_recipes = len(self.recipes)
        self.selected_recipe = self.recipes[0]

    def render_recipe(self, centre):
        start_x = centre[0] - self.total_width // 2
        start_y = centre[1] - self.square_size // 2 

        for i in range(self.number_of_squares): # Square

            # ----- OUTPUT -------
            if i == (self.number_of_squares - 1):
                x = start_x + i * (self.square_size + 8) - self.offset
                self.render_item(self.ds, self.selected_recipe["output"], x, start_y)
                break
            
            # ------ INPUTS -------
            x = start_x + i * (self.square_size + self.margin) - self.offset
            current_input = self.selected_recipe["input"][i]
            self.render_item(self.ds, current_input["id"], x, start_y, current_input["amt"], True)

        # ------- ARROW -------
        self.ds.blit(self.images[0], (self.midpoint[0] + 18, self.midpoint[1] - 19)) # Arrow

    def render_inventory(self, centre):
        # Rendering stuff
        n = min(3, len(self.open_tile.inventory))
        margin = 12
        offset = 8
        total_width = n * self.square_size + (n - 1) * margin
        start_x = centre[0] - total_width // 2
        start_y = centre[1] - self.square_size // 2 

        # Inventory
        inventory = self.open_tile.inventory
        inventory_ids = list(inventory.keys())

        for i in range(n): # Squares
            x = start_x + i * (self.square_size + margin)
            self.ds.blit(self.item_images[inventory_ids[i]], (x, start_y - offset))
            centred_text_at(self.ds, self.font, (x + (self.square_size * 0.5), start_y + self.square_size + 6 - offset), f"{inventory[inventory_ids[i]]}")

        # Empty button
        self.ds.blit(self.images[1], (self.midpoint[0] + self.half_width - 7, self.midpoint[1] + self.half_height - 7))
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] + self.half_width - 8, self.midpoint[1] + self.half_height - 8, 7, 7), 1)


    def render_item(self, surf, item, x, y, amt=0, input=False):
        surf.blit(self.item_images[item], (x, y))
        if input and amt != 0:
            centred_text_at(surf, self.font, (x + self.square_size, y), f'{amt}')

    def render_submenu(self):
        first_visable = math.floor((self.scroll + 1) / 22)
        start_x = self.submenu_midpoint[0] - self.total_width // 2
        start_y = 5 + (self.square_size + self.margin) * first_visable

        self.submenu_surface.fill((180, 180, 180))
        for i in range(min(self.total_recipes, 4)):

            recipe = self.recipes[first_visable + i]
            for j in range(self.number_of_squares): # Square
                y = start_y + i * (self.square_size + self.margin)

                # ------ OUTPUTS --------
                if j == (self.number_of_squares - 1):
                    self.submenu_surface.blit(self.images[0], (self.submenu_midpoint[0] + 18, y + 4 - self.scroll)) # Arrow
                    x = start_x + j * (self.square_size + (self.margin + 2)) - self.offset
                    self.render_item(self.submenu_surface, recipe["output"], x, y - self.scroll)
                    break

                # ------- INPUTS ------
                x = start_x + j * (self.square_size + self.margin) - self.offset
                current_input = recipe["input"][j]
                self.render_item(self.submenu_surface, current_input["id"], x, y - self.scroll, current_input["amt"], True)

        self.ds.blit(self.submenu_surface, (self.midpoint[0] - self.half_width + 2, self.midpoint[1] - self.half_height + 2))

    def mouse_event(self, mouseX, mouseY): # 188 65, 160 88
        if self.state == 1:
            if rectangle_collision((mouseX, mouseY, 1, 1), (self.midpoint[0] + 28, self.midpoint[1] - 23, 16, 16)):
                self.state = 2
            elif rectangle_collision((mouseX, mouseY, 1, 1), (self.midpoint[0] + self.half_width - 7, self.midpoint[1] + self.half_height - 7, 5, 5)):
                self.open_tile.inventory = {}

        elif self.state == 2:
            start_x = self.submenu_midpoint[0] - 41
            first_visable = math.floor((self.scroll + 1) / 22)
            distance = 5 + (16 + 6) * first_visable
            mouseX -= self.midpoint[0] - self.half_width
            mouseY -= self.midpoint[1] - self.half_height
            for i in range(4):
                rect = [start_x + 3 * (16 + 6) + 3, distance + i * (16 + 6) - self.scroll, 16, 16]
                if rectangle_collision((mouseX, mouseY, 1, 1), rect):
                    recipe = first_visable + i
                    self.selected_recipe = self.recipes[recipe]
                    self.open_tile.recipe = self.selected_recipe
                    self.state = 1


    def scroll_submenu(self, direction):
        self.scroll += direction * 5
        if self.scroll < 0 or self.total_recipes < 3:
            self.scroll = 0
        elif self.scroll > 9 + (16 + 6) * (self.total_recipes - 3) + 5:
            # 9 is the scroll when third tile ends, 16 = size, 6 = margin, 5 = start_margin
            self.scroll = 9 + (16 + 6) * (self.total_recipes - 3) + 5

    def render(self):
        pygame.draw.rect(self.ds, (180, 180, 180), (self.midpoint[0] - self.half_width, self.midpoint[1] - self.half_height, self.gui_width, self.gui_height))
        pygame.draw.rect(self.ds, (140, 140, 140), (self.midpoint[0] - self.half_width, self.midpoint[1] - self.half_height, self.gui_width, self.gui_height), 2)

        if self.state == 1:
            self.render_recipe((self.midpoint[0], self.midpoint[1] - (self.half_height * 0.5)))
            self.render_inventory((self.midpoint[0], self.quarter))
        else:
            self.render_submenu()