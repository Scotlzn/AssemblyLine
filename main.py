import pygame
from game import Game

pygame.init()
WINDOW_SIZE = (800, 800)
DISPLAY_SIZE = (96, 96)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.surface.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()
TITLE = "Assembly Line "
WINDOW_DATA = {
	"Upscale": WINDOW_SIZE[0] / DISPLAY_SIZE[0]
}

main = Game(display, WINDOW_DATA)

while True:
	dt = clock.tick(60) / 1000.0
	display.fill('black')	
	main.update(dt)
	pygame.display.set_caption(TITLE + str(clock.get_fps()))
	surf = pygame.transform.scale(display, WINDOW_SIZE)
	screen.blit(surf, (0, 0))
	pygame.display.update()