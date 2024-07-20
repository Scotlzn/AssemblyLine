import pygame, sys, math, time
from map import Map
from item import Item
from support import image_alpha, load_all_items, rectangle_collision, load_json
from editor import Editor
from ui import Ui
from tile import Tile

class Game:
    def __init__(self, ds, window_data):
        self.ds = ds
        self.window_data = window_data

        self.tile_size = 16
        self.item_size = 8

        self.money = 0

        self.item_images = load_all_items()
        self.recipes = load_json('./Data/recipes')

        self.map = Map(self.ds, self.tile_size)
        self.editor = Editor()
        self.ui = Ui(window_data, self.ds, self, self.item_images, self.recipes)

        self.timers = {
            'generator': time.time(),
            'crafter': time.time()
        }

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
    
    def can_craft(self, recipe, items):
        for ingredient in recipe["input"]:
            id = ingredient["id"]
            if id == 0: continue
            if id in items:
                if ingredient["amt"] <= items[id]:
                    continue
            return False
        return True
    
    def consume_items(self, recipe, tile):
        for input in recipe["input"]:
            id = input["id"]
            if id != 0:
                tile.inventory[id] -= 1
                if tile.inventory[id] == 0:
                    tile.inventory.pop(id, None)

    def spawn_item(self, id, rotation, x, y):
        new_item = Item(self.ds, id, self.item_images[id], (x * self.tile_size + (self.tile_size * 0.5) - (self.item_size * 0.5), y * self.tile_size + (self.tile_size * 0.5) - (self.item_size * 0.5)), self.map.tiles, self.tile_size, self.item_size, self.sell_item)
        movement = self.editor.get_movement_from_rotation(rotation)
        new_item.target_x = (x + movement[0]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - (self.item_size * 0.5)
        new_item.target_y = (y + movement[1]) * new_item.conveyor_size + (new_item.conveyor_size * 0.5) - (self.item_size * 0.5)
        self.items.append(new_item)

    def update_timers(self):
        current_time = time.time()

        # -------- UPDATE TIMERS ----------
        generator_timer = current_time > self.timers['generator'] + 1
        if generator_timer:
            self.timers['generator'] = current_time

        crafter_timer = current_time > self.timers['crafter'] + 1
        if crafter_timer:
            self.timers['crafter'] = current_time

        for y in range(self.map.height):
            for x in range(self.map.width):
                tile = self.map.tiles[y][x]
                if tile == 0: continue

                # ------------ ITEM SPAWNING ------------
                if generator_timer:
                    if tile.tile == 2: # Generator
                        self.spawn_item(tile.generating, tile.rotation, x, y)

                # ------------ CRAFTING ----------------
                if crafter_timer:
                    if tile.tile == 4: # Crafter
                        recipe = tile.recipe
                        if recipe != None and recipe["output"] != 0:
                            inventory = tile.inventory
                            if self.can_craft(recipe, inventory):
                                self.spawn_item(recipe["output"], tile.rotation, x, y)
                                self.consume_items(recipe, tile)


    # -------- Picking up items -------
    def pick_up_item(self, tile, mouseX, mouseY):
        if tile != 0 and tile.tile == 2: return
        for item in self.items:
            if item.colliding((mouseX, mouseY, 1, 1)):
                self.overlay = Item(self.ds, item.id, item.img, (mouseX - (self.item_size * 0.5), mouseY - (self.item_size * 0.5)), self.map.tiles, self.tile_size, self.item_size, self.sell_item, True)
                self.items.remove(item)
                break
    
    def sell_item(self, item_id):
        print(f'Sold item {item_id}')
        self.money += 1

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
                    self.ui.active = 0
                    self.editor.active = not self.editor.active

                if event.key == pygame.K_f:
                    self.items.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                mouseX, mouseY = self.get_mouse_pos()
                tileX = math.floor(mouseX / self.tile_size)
                tileY = math.floor(mouseY / self.tile_size)

                if event.button == 4:  # Mouse wheel up
                    self.ui.scroll(-1, mouseX, mouseY)
                    return
                elif event.button == 5:  # Mouse wheel down
                    self.ui.scroll(1, mouseX, mouseY)
                    return

                if tileY >= self.map.height: # HUD
                    self.ui.navbar.mouse_event(mouseX, mouseY)
                    return
                
                tile = self.map.tiles[tileY][tileX]
                
                if event.button == 1:
                    if self.editor.active:
                        # ---------- Placing conveyors ------------
                        if tile == 0:
                            self.map.tiles[tileY][tileX] = Tile(self.ds, (tileX * self.tile_size, tileY * self.tile_size), (self.editor.selected_tile, self.editor.rotation), self.tile_size, self.map.images[self.editor.get_correct_index()])
                        else:
                            self.map.tiles[tileY][tileX] = 0

                    else: # ----------- Pickup and UI -------------
                        self.pick_up_item(tile, mouseX, mouseY)
                        self.ui.mouse_event(tile, mouseX, mouseY)

            # ----------- DROPING ITEMS ----------
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                if event.button == 1:
                    if self.overlay != None:
                        self.items.append(Item(self.ds, self.overlay.id, self.overlay.img, (self.overlay.x, self.overlay.y), self.map.tiles, self.tile_size, self.item_size, self.sell_item))
                        self.overlay = None

    def update(self, dt):
        self.loop()

        self.update_timers()

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
            if tileY < self.map.height:
                tile = self.map.tiles[tileY][tileX]
                if tile == 0:
                    self.ds.blit(image_alpha(self.map.images[self.editor.get_correct_index()], 128), (tileX * self.tile_size, tileY * self.tile_size))
            
        self.ui.update()
