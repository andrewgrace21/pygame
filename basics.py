import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1500, 500))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (10, 10, 10))
textpos = text.get_rect().centerx
textpos.centerx = background.get_rect().centerx
background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    screen.blit(background, (0, 0))
    pygame.display.flip()