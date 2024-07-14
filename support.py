import pygame
from random import randint

def rectangle_collision(a, b):
    return (a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and a[1] + a[3] > b[1])

def generate_empty_map(size):
    out = []
    for y in range(size):
        nl = []
        for x in range(size):
            tile = 0
            # if randint(1, 2) == 1:
            #     tile = randint(1, 4)
            nl.append(tile)
        out.append(nl)
    return out

def image_alpha(source, opacity):
    temp = pygame.Surface((source.get_width(), source.get_height()), pygame.SRCALPHA)
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    return temp