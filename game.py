import pygame, sys, math, time
from map import Map
from item import Item
from support import image_alpha, rectangle_collision, load_all_items, any_value_true, ui_active_to_data, set_all_false
from editor import Editor
from ui import Ui
from tile import Tile

class Game:
    def __init__(self, ds, window_data):
        self.ds = ds
        self.window_data = window_data

        self.tile_size = 16
        self.item_size = 8

        self.item_images = load_all_items()

        self.map = Map(self.ds, self.tile_size)
        self.editor = Editor()
        self.ui = Ui(self.ds, self)

        self.last_time = time.time()

        self.items = []
        self.mouse_down = False
        self.overlay = None

    def get_mouse_pos(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = math.floor(mouseX / self.window_data["Upscale"])
        mouseY = math.floor(mouseY / self.window_data["Upscale"])
        return mouseX, mouseY

    def get_tile_at(self):
        mx, my = self.get_mouse_pos()
        tx = math.floor(mx / self.tile_size)
        ty = math.floor(my / self.tile_size)
        return tx, ty
        

    def timers(self):
        current_time = time.time()
        if current_time > self.last_time + 1:
            self.last_time = current_time
            for y in range(self.map.size):
                for x in range(self.map.size):
                    tile = self.map.tiles[y][x]
                    # ------------ ITEM SPAWNING ------------
                    if tile != 0 and tile.tile == 2: # Generator
                        new_item = Item(self.ds, tile.generating, self.item_images[tile.generating], (x * self.tile_size + (self.tile_size * 0.5) - (self.item_size * 0.5), y * self.tile_size + (self.tile_size * 0.5) - (self.item_size * 0.5)), self.map.tiles, self.tile_size, self.item_size)
                        movement = self.editor.get_movement_from_rotation(tile.rotation)
                        new_item.target_x = (x + movement[0]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - (self.item_size * 0.5)
                        new_item.target_y = (y + movement[1]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - (self.item_size * 0.5)
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
                tileX = math.floor(mouseX / self.tile_size)
                tileY = math.floor(mouseY / self.tile_size)
                tile = self.map.tiles[tileY][tileX]
                
                if event.button == 1:
                    for item in self.items: # Picking up items
                        if item.colliding((mouseX, mouseY, 1, 1)):
                            self.overlay = Item(self.ds, 1, self.item_images[1], (mouseX - (self.item_size * 0.5), mouseY - (self.item_size * 0.5)), self.map.tiles, self.tile_size, self.item_size, True)
                            self.items.remove(item)
                            break
                    
                    # ----------- UI -------------
                    if not any_value_true(self.ui.active):
                        if tile != 0:
                            if tile.tile == 4:
                                self.ui.active["crafter"] = True
                                self.ui.crafter_ui.open_tile = tile
                            elif tile.tile == 2:
                                self.ui.active["generator"] = True
                                self.ui.generator_ui.open_tile = tile
                                self.ui.generator_ui.current_item = tile.generating

                    else:
                        midpoint = 192 * 0.5
                        ui_data = [[98, 60], [64, 64]]
                        index = ui_active_to_data(self.ui.active)
                        gui_width = ui_data[index][0]
                        gui_height = ui_data[index][1]
                        if not rectangle_collision((mouseX, mouseY, 1, 1), (midpoint - (gui_width*0.5), midpoint - (gui_height*0.5), gui_width, gui_height)):
                            set_all_false(self.ui.active)
                        else:
                            self.ui.submenus(mouseX, mouseY)

                # Placing conveyors
                elif event.button == 3 and self.editor.active:
                    if tile == 0:
                        self.map.tiles[tileY][tileX] = Tile(self.ds, (tileX * self.tile_size, tileY * self.tile_size), (self.editor.selected_tile, self.editor.rotation), self.tile_size, self.map.images[self.editor.get_correct_index()])
                    else:
                        self.map.tiles[tileY][tileX] = 0

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                if event.button == 1:
                    if self.overlay != None:
                        self.items.append(Item(self.ds, 1, self.item_images[1], (self.overlay.x, self.overlay.y), self.map.tiles, self.tile_size, self.item_size))
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
            self.overlay.x = mouseX - (self.item_size * 0.5)
            self.overlay.y = mouseY - (self.item_size * 0.5)
            self.overlay.update(dt)

        elif self.editor.active: # Placing outline
            tileX, tileY = self.get_tile_at()
            tile = self.map.tiles[tileY][tileX]
            if tile == 0:
                self.ds.blit(image_alpha(self.map.images[self.editor.get_correct_index()], 128), (tileX * self.tile_size, tileY * self.tile_size))
            
        self.ui.update()