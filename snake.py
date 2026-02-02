import pygame
from pygame.locals import *
import numpy as np
pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w,pygame.display.Info().current_h-50))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

grid = pygame.Surface(screen.get_size())
grid_size = (15,9)
rect_size = 60
cent_start = np.divide(np.subtract(screen.get_size(),np.multiply(grid_size,rect_size)),2).astype(int)
dims = grid_size*rect_size
rects = [[pygame.Rect(row*rect_size+cent_start[0],col*rect_size+cent_start[1],rect_size,rect_size) for col in range(grid_size[1])] for row in range(grid_size[0])]

num_apples = 5
def apple_pos(num):
    list = []
    for _ in range(num):
        pos = [np.random.randint(grid_size[0]),np.random.randint(grid_size[1])]
        while pos in snake or pos in list:
            pos = [np.random.randint(grid_size[0]),np.random.randint(grid_size[1])]
        list.append(pos)
    return list

screen.blit(background, (0,0))
snake = [[i,grid_size[1]//2] for i in range(4,7)]
move = [1,0]
apple = apple_pos(num_apples)

for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        if ([i,j]) in snake:
            green = (0, 255-100/(len(snake)-1)*snake.index([i,j]), 0)
            pygame.draw.rect(screen, green, rects[i][j])
            pygame.draw.rect(screen, (0,0,0), rects[i][j], width=1)
        elif ([i,j]) in apple:
            pygame.draw.rect(screen, (255,0,0), rects[i][j])
            pygame.draw.rect(screen, (0,0,0), rects[i][j], width=1)
        else:
            pygame.draw.rect(screen, (0,0,0), rects[i][j], width=1)

pygame.display.flip()
clock = pygame.time.Clock()
fps = 7
dead = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            
    if not dead:
        for event in reversed(events):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if move != [0,1]:
                        move = [0,-1]
                        break
                elif event.key == pygame.K_RIGHT:
                    if move != [-1,0]:
                        move = [1,0]
                        break
                elif event.key == pygame.K_DOWN:
                    if move != [0,-1]:
                        move = [0,1]
                        break
                elif event.key == pygame.K_LEFT:
                    if move != [1,0]:
                        move = [-1,0]
                        break
                        
        new = np.add(snake[-1],move).tolist()
        if new not in snake and new[0]>=0 and new[0]<grid_size[0] and new[1]>=0 and new[1]<grid_size[1]:
            snake = snake + [new]
            
            ate = False
            for i in range(len(apple)):
                if apple[i] in snake:
                    apple[i] = apple_pos(1)[0]
                    pygame.draw.rect(screen, (255,0,0), rects[apple[i][0]][apple[i][1]])
                    pygame.draw.rect(screen, (0,0,0), rects[apple[i][0]][apple[i][1]], width=1)
                    pygame.display.update(rects[apple[i][0]][apple[i][1]])
                    ate = True
            if not ate:
                pygame.draw.rect(screen, (255,255,255), rects[snake[0][0]][snake[0][1]])
                pygame.draw.rect(screen, (0,0,0), rects[snake[0][0]][snake[0][1]], width=1)
                pygame.display.update(rects[snake[0][0]][snake[0][1]])
                snake = snake[1:]
            for index,cell in enumerate(snake):
                green = (0, 255-100/(len(snake)-1)*index, 0)
                pygame.draw.rect(screen, green, rects[cell[0]][cell[1]])
                pygame.draw.rect(screen, (0,0,0), rects[cell[0]][cell[1]], width=1)
            pygame.display.update([rects[cell[0]][cell[1]] for cell in snake])
            
        else:
            dead = True
            game_over = pygame.font.Font(None,56).render("Game Over", 1, (0,0,0))
            text_box = game_over.get_rect(center=(screen.get_rect().centerx, cent_start[1]/2))
            screen.blit(game_over, text_box)
            pygame.display.update(text_box)
        
        clock.tick(fps)
