import pygame, time
import math
from support import rectangle_collision, opposite_direction, selector_direction

class Item:
    def __init__(self, ds, id, img, pos, conveyors, tunnels, tile_size, size, sell_func, overlay=False):
        self.ds = ds
        self.conveyors = conveyors
        self.size = size
        self.overlay = overlay

        self.tunnels = tunnels

        self.id = id
        self.img = img

        self.sell_func = sell_func

        self.x = pos[0]
        self.y = pos[1]
        self.target_x = self.x
        self.target_y = self.y
        self.direction = None

        self.despawn = False
        self.delete = False
        self.despawn_time = None

        self.conveyor_speed = 44
        self.conveyor_size = tile_size

        self.visible = True

        self.conveyor_directions = {
            1: (0, 1),   # Down
            2: (-1, 0),  # Left
            3: (0, -1),   # Up
            4: (1, 0)   # Right
        }

    def colliding(self, rect):
        if rectangle_collision(rect, (self.x, self.y, self.size, self.size)):
            return True
        return False

    def bounds_check(self):
        if self.x < 0:
            self.x = 0
            if (self.despawn_time == None): self.despawn = True
        if self.y < 0:
            self.y = 0
            if (self.despawn_time == None): self.despawn = True
        if self.x > 640 - self.size:
            self.x = 640 - self.size
            if (self.despawn_time == None): self.despawn = True
        if self.y > 352 - self.size:
            self.y = 352 - self.size
            if (self.despawn_time == None): self.despawn = True

    def despawn_timer(self):
        if time.time() > self.despawn_time:
            self.delete = True

    def despawn_checks(self):
        if self.despawn:
            self.despawn_time = time.time() + 5
            self.despawn = False
        if self.despawn_time != None:
            self.despawn_timer()

    def schedule_to_despawn(self):
        if self.despawn_time == None: self.despawn = True

    def enter_inventory(self, data):
        inventory = data.inventory
        if self.id in inventory:
            inventory[self.id] += 1
        else:
            inventory[self.id] = 1

    def move_to(self, x, y, direction):
        movement = self.conveyor_directions[direction]
        # Set new target to conveyor direction * conveyor size + (middle of conveyor) + (middle of item)
        self.target_x = (x + movement[0]) * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)
        self.target_y = (y + movement[1]) * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)
        self.direction = direction

    def change_target(self):
        # Get all the data about tile we are on and where we came from
        tileX = math.floor(self.x / self.conveyor_size)
        tileY = math.floor(self.y / self.conveyor_size)
        tile_data = self.conveyors[tileY][tileX]

        # Remove all empty tiles before getting data from objects to not cause errors :D
        if tile_data == 0: 
            self.schedule_to_despawn()
            return

        tile = tile_data.tile
        previous_direction = self.direction
        self.direction = tile_data.rotation

        if tile == 1: # Conveyor and tunnel out
            if not self.overlay:
                self.move_to(tileX, tileY, self.direction)

        elif tile == 3: # Seller
            self.sell_func(self.id)
            self.delete = True # Delete

        elif tile in [4, 5, 6, 7, 8]: # Crafters
            incident_direction = opposite_direction(self.direction)
            if incident_direction != previous_direction: # If item enters tile via valid direction
                self.enter_inventory(tile_data)
            self.delete = True

        elif tile in [9, 10]: # Selectors 2 (9) and 3 (10)
            incident_direction = opposite_direction(self.direction)
            if incident_direction == previous_direction: # If item enters crafter via bottom
                tile_data.split = selector_direction(tile_data.split, (tile - 9) + 2) # Update splitter path
                self.move_to(tileX, tileY, opposite_direction(tile_data.split, tile_data.rotation - 1))
            else: self.delete = True

        elif tile in [11, 12]: # Splitter
            direction = {11: 1, 12: 3}
            if tile_data.recipe != self.id:
                self.move_to(tileX, tileY, opposite_direction(self.direction)) # Splitter is reversed
            else:
                self.move_to(tileX, tileY, opposite_direction(self.direction, direction[tile])) # Left or Right

        elif tile == 13: # Tunnel In
            if (tileX, tileY) in self.tunnels:
                pos = self.tunnels[(tileX, tileY)]
                self.target_x = pos[0] * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)
                self.target_y = pos[1] * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)
                self.direction = self.direction
                self.visible = False
            else: self.schedule_to_despawn()

        elif tile == 14: # Tunnel Out
            self.move_to(tileX, tileY, self.direction)
            self.visible = True

        else: self.schedule_to_despawn() # Ground or unknown tile

    def move(self, dt):
        # Dont calculate anything while an overlay or it will cause bugs
        if self.overlay: return
        # Change target to next conveyor if target has been reached (by target I mean centre)
        if self.x == self.target_x and self.y == self.target_y:
            self.change_target()

        # If position is not target then get the minimum of movement and the distance to target
        # This means it will move if distance to target != 0
        if self.x < self.target_x:
            self.x += min(self.conveyor_speed * dt, self.target_x - self.x)
        elif self.x > self.target_x:
            self.x -= min(self.conveyor_speed * dt, self.x - self.target_x)

        if self.y < self.target_y:
            self.y += min(self.conveyor_speed * dt, self.target_y - self.y)
        elif self.y > self.target_y:
            self.y -= min(self.conveyor_speed * dt, self.y - self.target_y)

    def render(self):
        if self.visible:
            self.ds.blit(self.img, (self.x, self.y))

    def update(self, dt):
        self.move(dt)
        self.bounds_check()
        self.render()
        self.despawn_checks()