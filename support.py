import pygame, json, math
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

def opposite_direction(n, by=2):
    return (n + by - 1) % 4 + 1

selector2 = {4: 2,2: 4}
selector3 = {4: 2,2: 3,3: 4}
def selector_direction(direction, selector):
    if selector == 2:
        return selector2[direction]
    elif selector == 3:
        return selector3[direction]

def load_json(path):
    data = json.load(open(path+'.json'))
    return data

def load_prices():
    out = {}
    data = load_json('./Data/prices')
    for key, value in data.items():
        out[int(key)] = value
    return out

def render_tunnel_path(surf, tileX, tileY, tunnel):
        # Dont render the tunnel path if it is not straight, or behind entrance
        distance = 0
        # ----- Check direction -------
        if tunnel[2] in [1, 3]:
            if tileX != tunnel[0]: return False
            distance = tileY - tunnel[1]
        if tunnel[2] in [2, 4]:
            if tileY != tunnel[1]: return False
            distance = tileX - tunnel[0]
        # ----- Check overall distance to centre -----
        if abs(distance) < 2: return False
        # ----- Check if tile is in the wrong direction ------
        if distance < 0 and tunnel[2] in [2, 3]: return False
        if distance > 0 and tunnel[2] in [1, 4]: return False
        # ----- Render in the right direction -----
        if tunnel[2] == 2:
            pygame.draw.rect(surf, (255, 0, 0), (tunnel[0] * 16 + (16 * math.copysign(1, distance)), tunnel[1] * 16, (distance-1) * 16, 16))
        elif tunnel[2] == 4:
            pygame.draw.rect(surf, (255, 0, 0), (tileX * 16 + (-16 * math.copysign(1, distance)), tileY * 16, (-distance-1) * 16, 16))
        elif tunnel[2] == 3:
            pygame.draw.rect(surf, (255, 0, 0), (tunnel[0] * 16, (tunnel[1] * 16 + (16 * math.copysign(1, distance))), 16, (distance-1)*16))
        else:
            pygame.draw.rect(surf, (255, 0, 0), (tileX * 16, (tileY * 16 + (-16 * math.copysign(1, distance))), 16, (-distance-1)*16))
        return True