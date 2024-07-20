import pygame, json
from random import randint

def rectangle_collision(a, b):
    return (a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and
            a[1] < b[1] + b[3] and a[1] + a[3] > b[1])

def generate_empty_map(w, h):
    out = []
    for y in range(h):
        nl = []
        for x in range(w):
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

def load_all_items(items=4):
    out = {}
    for i in range(1, items+1, 1):
        out[i] = pygame.image.load(f'Assets/Items/{i}.png').convert()
    return out

def any_value_true(dictionary):
    return any(dictionary.values())

def ui_active_to_data(actives):
    if actives["crafter"]:
        return 0
    if actives["generator"]:
        return 1
    
def set_all_false(dictionary):
    for key in dictionary:
        dictionary[key] = False
    return dictionary

def centred_text_at(surf, font, pos, text):
        textSurface = font.render(text, False, (255, 255, 255))
        textRect = textSurface.get_rect(center=pos)
        surf.blit(textSurface, textRect)

def opposite_direction(n):
    return (n + 2 - 1) % 4 + 1

def load_json(path):
    data = json.load(open(path+'.json'))
    return data