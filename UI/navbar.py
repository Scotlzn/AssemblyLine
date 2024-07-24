import pygame
from support import rectangle_collision, centred_text_at, add_suffix

class Navbar:
    def __init__(self, ds, game, font, tile_images):
        self.ds = ds
        self.game = game
        self.font = font
        self.tile_images = tile_images
        self.editor = game.editor

        self.images = [
            pygame.image.load('./Assets/build.png').convert(),
            pygame.image.load('./Assets/upgrade.png').convert(),
            pygame.image.load('./Assets/settings.png').convert(),
            pygame.image.load('./Assets/tutorial.png').convert()
        ]

        for i, img in enumerate(self.images):
            self.images[i] = pygame.transform.scale(img, (32, 32))

        self.state = 2 # 1 = Main, 2 = Build,

        # ------- TILES LAYOUT -------
        self.normal_tiles = [1, 2, 3, 4, 5, 6, 8, 10, 11, 13]
        self.extra_tiles = [1, 2, 3, 4, 5, 6, 7, 9, 12, 13]
        self.displayed_tiles = self.normal_tiles

        self.rect = (0, 384-32, 640, 32)

    def mouse_event(self, mouseX, mouseY):
        # ------- Build Icon -------
        if rectangle_collision((mouseX, mouseY, 1, 1), (0, 352, 32, 32)):
            new_state = 1 if self.state == 2 else 2
            self.state = new_state

        elif self.state == 1:
            pass

        elif self.state == 2:
            # ------- Tile selection checks ------
            for i in range(1, len(self.displayed_tiles) + 1):
                if rectangle_collision((mouseX, mouseY, 1, 1), (i * 32 + (i * 1), 352, 32, 32)):
                    self.editor.selected_tile = self.displayed_tiles[i - 1]

    def build(self):
        for i in range(1, len(self.displayed_tiles) + 1):
            tile = self.tile_images[((self.displayed_tiles[i - 1] - 1) * 4) + 1]
            self.ds.blit(tile, (i * (32 + 2), 352))

    def main(self):
        for i in range(1, 4):
            self.ds.blit(self.images[i], (i * (32 + 2), 352))

    def render(self):
        pygame.draw.rect(self.ds, '#333333', self.rect)
        self.ds.blit(self.images[0], (0, 352))

        if self.state == 2:
            self.build()
        else:
            self.main()

        centred_text_at(self.ds, self.font, (460, 384-16), f'M/S: {add_suffix(self.game.mps)}')
        centred_text_at(self.ds, self.font, (580, 384-16), f'Money: {add_suffix(self.game.money)}')

    def update(self):
        self.render()