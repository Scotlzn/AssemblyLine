import pygame, time
import math
from support import rectangle_collision, opposite_direction

class Item:
    def __init__(self, ds, id, img, pos, conveyors, tile_size, size, overlay=False):
        self.ds = ds
        self.conveyors = conveyors
        self.size = size
        self.overlay = overlay

        self.id = id
        self.img = img

        self.x = pos[0]
        self.y = pos[1]
        self.target_x = self.x
        self.target_y = self.y
        self.direction = None

        self.despawn = False
        self.delete = False
        self.despawn_time = None

        self.conveyor_speed = 20
        self.conveyor_size = tile_size

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
        if self.x > 192 - self.size:
            self.x = 192 - self.size
            if (self.despawn_time == None): self.despawn = True
        if self.y > 192 - self.size:
            self.y = 192 - self.size
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
        inventory[self.id] += 1

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

        if tile == 1: # Conveyor
            if not self.overlay:
                movement = self.conveyor_directions[self.direction]
                # Set new target to conveyor direction * conveyor size + (middle of conveyor) + (middle of item)
                self.target_x = (tileX + movement[0]) * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)
                self.target_y = (tileY + movement[1]) * self.conveyor_size + (self.conveyor_size * 0.5) - (self.size * 0.5)

        elif tile == 3: # Seller
            self.delete = True # Delete

        elif tile == 4: # Crafter
            incident_direction = opposite_direction(self.direction)
            if incident_direction != previous_direction: # If item enters crafter via valid direction
                self.enter_inventory(tile_data)
            self.delete = True

        else: self.schedule_to_despawn() # Ground or unknown tile

    def move(self, dt):
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

        self.bounds_check()

    def render(self):
        self.ds.blit(self.img, (self.x, self.y))

    def update(self, dt):
        self.move(dt)
        self.render()
        self.despawn_checks()