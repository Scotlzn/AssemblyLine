import pygame, sys, math, time
from map import Map
from item import Item
from support import image_alpha, rectangle_collision
from editor import Editor
from ui import Ui

class Game:
    def __init__(self, ds, window_data):
        self.ds = ds
        self.window_data = window_data

        self.map = Map(self.ds)
        self.editor = Editor()
        self.ui = Ui(self.ds, self)

        self.last_time = time.time()

        self.items = [Item(self.ds, self.map.tiles, (32, 32)), Item(self.ds, self.map.tiles, (64, 64))]
        self.mouse_down = False
        self.overlay = None

    def get_mouse_pos(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = math.floor(mouseX / self.window_data["Upscale"])
        mouseY = math.floor(mouseY / self.window_data["Upscale"])
        return mouseX, mouseY

    def get_tile_at(self):
        mx, my = self.get_mouse_pos()
        tx = math.floor(mx / 8)
        ty = math.floor(my / 8)
        return tx, ty
        

    def timers(self):
        current_time = time.time()
        if current_time > self.last_time + 1:
            self.last_time = current_time
            for y in range(12):
                for x in range(12):
                    tile = self.map.tiles[y][x]
                    if tile in [5, 6, 7, 8]: # Generators
                        new_item = Item(self.ds, self.map.tiles, (x * 8 + (8 * 0.5) - (4 * 0.5), y * 8 + (8 * 0.5) - (4 * 0.5)))
                        movement = self.editor.get_movement_from_rotation(tile - 4)
                        new_item.target_x = (x + movement[0]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - 2
                        new_item.target_y = (y + movement[1]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - 2
                        self.items.append(new_item)


    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_q:
                    self.editor.change_rotation(1)

                if event.key == pygame.K_e:
                    self.editor.change_rotation(-1)

                if event.key == pygame.K_1:
                    self.editor.selected_tile = 1

                if event.key == pygame.K_2:
                    self.editor.selected_tile = 2
                
                if event.key == pygame.K_3:
                    self.editor.selected_tile = 3

                if event.key == pygame.K_4:
                    self.editor.selected_tile = 4

                if event.key == pygame.K_SPACE:
                    self.editor.active = not self.editor.active

                if event.key == pygame.K_f:
                    self.items.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                mouseX, mouseY = self.get_mouse_pos()
                tileX = math.floor(mouseX / 8)
                tileY = math.floor(mouseY / 8)
                tile = self.map.tiles[tileY][tileX]
                
                if event.button == 1:
                    for item in self.items: # Picking up items
                        if item.colliding((mouseX, mouseY, 1, 1)):
                            self.overlay = Item(self.ds, self.map.tiles, (mouseX - 2, mouseY - 2), True)
                            self.items.remove(item)
                            break
                    
                    if self.ui.active["crafter"] == False:
                        if tile in [13, 14, 15, 16]:
                            self.ui.active["crafter"] = True
                    else:
                        midpoint = 96 * 0.5
                        if not rectangle_collision((mouseX, mouseY, 1, 1), (midpoint - 16, midpoint - 16, 32, 32)):
                            self.ui.active["crafter"] = False

                # Placing conveyors
                elif event.button == 3 and self.editor.active:
                    if tile == 0:
                        self.map.tiles[tileY][tileX] = self.editor.get_correct_index()
                    else:
                        self.map.tiles[tileY][tileX] = 0

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                if event.button == 1:
                    if self.overlay != None:
                        self.items.append(Item(self.ds, self.map.tiles, (self.overlay.x, self.overlay.y)))
                        self.overlay = None

    def update(self, dt):
        self.loop()

        self.timers()

        self.map.update()

        for item in self.items[:]:
            item.update(dt)
            if item.delete:
                self.items.remove(item)

        if self.overlay != None:
            mouseX, mouseY = self.get_mouse_pos()
            self.overlay.x = mouseX - 2
            self.overlay.y = mouseY - 2
            self.overlay.update(dt)

        elif self.editor.active: # Placing outline
            tileX, tileY = self.get_tile_at()
            tile = self.map.tiles[tileY][tileX]
            if tile == 0:
                self.ds.blit(image_alpha(self.map.images[self.editor.get_correct_index()], 128), (tileX * 8, tileY * 8))
            
        self.ui.update()