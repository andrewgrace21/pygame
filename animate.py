import pygame
from pygame.locals import *
import numpy as np
pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w,pygame.display.Info().current_h-50))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

grid = pygame.Surface(screen.get_size())
grid_size = (35,25)
rect_size = 30
cent_start = np.divide(np.subtract(screen.get_size(),np.multiply(grid_size,rect_size)),2).astype(int)
dims = grid_size*rect_size
rects = [[pygame.Rect(row*rect_size+cent_start[0],col*rect_size+cent_start[1],rect_size,rect_size) for col in range(grid_size[1])] for row in range(grid_size[0])]

screen.blit(background, (0,0))
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        pygame.draw.rect(screen, (0,0,0), rects[i][j], width=1)
pygame.display.flip()
    
frame = 0
clock = pygame.time.Clock()
fps = 30
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    for j in range(grid_size[1]):
        pygame.draw.rect(screen, (0,0,0), rects[frame%grid_size[0]][j])
        pygame.draw.rect(screen, (255,255,255), rects[(frame-1)%grid_size[0]][j])
        pygame.draw.rect(screen, (0,0,0), rects[(frame-1)%grid_size[0]][j], width=1)
    pygame.display.update([rects[frame%grid_size[0]][j] for j in range(grid_size[1])])
    pygame.display.update([rects[(frame-1)%grid_size[0]][j] for j in range(grid_size[1])])
    clock.tick(fps)
    frame += 1
