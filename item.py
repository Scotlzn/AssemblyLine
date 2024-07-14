import pygame, time
import math
from support import rectangle_collision

class Item:
    def __init__(self, ds, conveyors, pos, overlay=False):
        self.ds = ds
        self.conveyors = conveyors
        self.overlay = overlay

        self.x = pos[0]
        self.y = pos[1]
        self.target_x = self.x
        self.target_y = self.y

        self.despawn = False
        self.delete = False
        self.despawn_time = None

        self.conveyor_speed = 10
        self.conveyor_size = 8

        self.conveyor_directions = {
            1: (0, 1),   # Down
            2: (-1, 0),  # Left
            3: (0, -1),   # Up
            4: (1, 0)   # Right
        }

    def colliding(self, rect):
        if rectangle_collision(rect, (self.x, self.y, 4, 4)):
            return True
        return False

    def bounds_check(self):
        if self.x < 0:
            self.x = 0
            if (self.despawn_time == None): self.despawn = True
        if self.y < 0:
            self.y = 0
            if (self.despawn_time == None): self.despawn = True
        if self.x > 96 - 4:
            self.x = 92
            if (self.despawn_time == None): self.despawn = True
        if self.y > 96 - 4:
            self.y = 92
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

    def move(self, dt):
        # Change target to next conveyor if target has been reached (by target I mean centre)
        if self.x == self.target_x and self.y == self.target_y:
            tileX = math.floor(self.x / self.conveyor_size)
            tileY = math.floor(self.y / self.conveyor_size)
            tile = self.conveyors[tileY][tileX]

            if tile in [1, 2, 3, 4]: # Conveyor
                if not self.overlay:
                    movement = self.conveyor_directions[tile]
                    # Set new target to conveyor direction * conveyor size + (middle of conveyor) + (middle of item)
                    self.target_x = (tileX + movement[0]) * self.conveyor_size + (self.conveyor_size * 0.5) - 2
                    self.target_y = (tileY + movement[1]) * self.conveyor_size + (self.conveyor_size * 0.5) - 2

            elif tile in [9, 10, 11, 12]: # Seller
                self.delete = True # Delete

            elif tile in [13, 14, 15, 16]: # Crafter
                self.delete = True

            elif self.despawn_time == None: self.despawn = True # Ground or unknown tile

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
        pygame.draw.rect(self.ds, (255, 255, 255), (self.x, self.y, 4, 4))

    def update(self, dt):
        self.move(dt)
        self.render()
        self.despawn_checks()