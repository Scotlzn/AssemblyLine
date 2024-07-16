import pygame
from support import centred_text_at

class Crafter_Ui:
    def __init__(self, ds, font):
        self.ds = ds
        self.font = font
        self.open_tile = None

        self.images = [
            pygame.image.load('./Assets/ui_pointer.png').convert()
        ]

    def render_recipe(self, centre):
        n = 4
        square_size = 16
        margin = 6
        offset = 3
        total_width = n * square_size + (n - 1) * margin
        start_x = centre[0] - total_width // 2
        start_y = centre[1] - square_size // 2 

        for i in range(n): # Square
            if i == (n - 1):
                margin = 8
            x = start_x + i * (square_size + margin) - offset
            pygame.draw.rect(self.ds, (255, 0, 0), (x, start_y, square_size, square_size))

        self.ds.blit(self.images[0], (114, 77)) # Arrow

    def render_inventory(self, centre):
        # Rendering stuff
        n = len(self.open_tile.inventory)
        square_size = 16
        margin = 12
        offset = 8
        total_width = n * square_size + (n - 1) * margin
        start_x = centre[0] - total_width // 2
        start_y = centre[1] - square_size // 2 

        # Inventory
        inventory_quantities = list(self.open_tile.inventory.values())

        for i in range(n): # Squares
            x = start_x + i * (square_size + margin)
            pygame.draw.rect(self.ds, (255, 0, 0), (x, start_y - offset, square_size, square_size))
            centred_text_at((x + (square_size * 0.5) + 1, start_y + square_size + 6 - offset), f"{inventory_quantities[i]}")

    def render(self):
        midpoint = 192 * 0.5
        gui_width = 98
        gui_height = 60
        half_width = gui_width * 0.5
        half_height = gui_height * 0.5
        lm = midpoint + (half_height * 0.5)

        pygame.draw.rect(self.ds, (180, 180, 180), (midpoint - half_width, midpoint - half_height, gui_width, gui_height))
        pygame.draw.rect(self.ds, (140, 140, 140), (midpoint - half_width, midpoint - half_height, gui_width, gui_height), 2)
        # pygame.draw.line(self.ds, (140, 140, 140), (midpoint - half, midpoint), (midpoint + (half - 1), midpoint))
        # pygame.draw.line(self.ds, (140, 140, 140), (midpoint, midpoint - half_height), (midpoint, midpoint + (half_height - 1)))

        self.render_recipe((midpoint, midpoint - (half_height * 0.5)))
        self.render_inventory((midpoint, lm))