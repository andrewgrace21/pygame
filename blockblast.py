import pygame
from pygame.locals import *
import numpy as np
import math
pygame.init()

def v_gradient(w,h,top_c,bot_c,trans=255):
    temp = pygame.Surface((w,h), pygame.SRCALPHA)
    for y in range(h):
        y = float(y)
        new_c = list(np.array(top_c)*(1-y/h)+np.array(bot_c)*(y/h)) + [trans]
        pygame.draw.line(temp, new_c, (0,y), (w,y))
    return temp

def orientations(list):
    new = []
    for index,item in enumerate(list):
        new.append([])
        for flip in [False,True]:
            temp = item
            if flip:
                temp = temp[::-1]
            new[index].append(temp)
            rot1 = [[temp[i][j] for i in range(np.shape(temp)[0])] for j in reversed(range(np.shape(temp)[1]))]
            new[index].append(rot1)
            rot2 = [[temp[i][j] for j in reversed(range(np.shape(temp)[1]))] for i in reversed(range(np.shape(temp)[0]))]
            new[index].append(rot2)
            rot3 = [[temp[i][j] for i in reversed(range(np.shape(temp)[0]))] for j in range(np.shape(temp)[1])]
            new[index].append(rot3)
    return new

def new_piece(center, scale=1):
    probabilities = [0.0435, 0.1166, 0.0417, 0.1068, 0.0658, 0.138, 0.0453, 0.13, 0.0899, 0.1603, 0.0293, 0.0097, 0.0211, 0.001, 0.001]
    piece_id = np.random.choice(range(len(possible)), p=probabilities)
    fill_map = possible[piece_id][np.random.randint(len(possible[piece_id]))]
    c = np.random.choice(['red','orange','yellow','green','light_blue','dark_blue','purple'])
    piece = pygame.sprite.Group()
    for i in range(np.shape(fill_map)[0]):
        for j in range(np.shape(fill_map)[1]):
            if fill_map[i][j]==1:
                piece.add(Block(center, np.shape(fill_map), index=[i,j], color=c, scale=scale))
    return piece

def can_place(piece):
    found = False
    for row in range(8):
        for col in range(8):
            open = True
            for sprite in piece.sprites():
                loc = np.add(sprite.index, (row,col))
                if 0<=loc[0]<8 and 0<=loc[1]<8:
                    if any([np.array_equal(loc, np.array(cell.index)) for cell in board]):
                        open = False
                        break
                else:
                    open = False
                    break
            if open:
                found = True
                break
        if found:
            break
    if not piece:
        found = False
    return found

start_size = .5
def reset_pieces():
    temp = [new_piece(three_center[0], start_size), new_piece(three_center[1], start_size), new_piece(three_center[2], start_size)]
    if not any([can_place(temp[i]) for i in range(3)]):
        while not any([can_place(temp[i]) for i in range(3)]):
            rand_num = np.random.randint(3)
            temp[rand_num] = new_piece(three_center[rand_num], start_size)
    return temp
    
unique = [[[1,0],[1,1],[0,1]],
          [[1,0],[1,0],[1,1]],
          [[1,1],[1,1]],
          [[1,1,1,1]],
          [[1,1,1]],
          [[1,1,1,1,1]],
          [[1,1,1],[0,1,0]],
          [[1,1,1],[1,1,1],[1,1,1]],
          [[1,0,0],[1,0,0],[1,1,1]],
          [[1,1,1],[1,1,1]],
          [[1,0],[1,1]],
          [[1,0,0],[0,1,0],[0,0,1]],
          [[1,1]],
          [[1]],
          [[1,0],[0,1]]]


possible = orientations(unique)

# outline, upper, lower
block_colors = {'black':[(0,0,0), (80,80,80), (60,60,60)],
                'red':[(122, 24, 23), (233, 74, 66), (211, 48, 47)],
                'orange':[(125, 41, 0), (253, 112, 44), (231, 73, 0)],
                'yellow':[(103, 50, 0), (248, 203, 17), (242, 175, 0)],
                'green':[(0, 74, 20), (55, 219, 36), (0, 176, 50)],
                'light_blue':[(2, 67, 93), (51, 209, 248), (0, 184, 231)],
                'dark_blue':[(32, 44, 115), (68, 109, 243), (41, 82, 237)],
                'purple':[(70, 0, 101), (161, 94, 231), (134, 70, 225)],
                'no_space':[(35, 48, 97), (66, 90, 164), (64, 87, 159)]}

desktop = pygame.display.Info()
#screen = pygame.display.set_mode((desktop.current_w,desktop.current_h-50))
screen = pygame.display.set_mode((700,desktop.current_h-50))
cell_size = int(desktop.current_h/15)
background = pygame.Surface((8*cell_size,8*cell_size))
back_rect = background.get_rect()
back_rect.center = screen.get_rect().center
back_rect.centery *= .85
border_w = 2
inner_prop = .66
offset = 4
font = "static/LeagueSpartan-SemiBold.ttf"

class Block(pygame.sprite.Sprite):
    def __init__(self, center, size, index=[0,0], color='black', scale=1, trans=255):
        super().__init__()
        self.image = pygame.Surface((cell_size*scale, cell_size*scale), pygame.SRCALPHA)
        self.color = block_colors[color]
        self.scale = scale
        self.index = index
        self.center = center
        self.size = size
        self.trans = trans
        self.board = False
        self.pos = (np.array(self.center) - np.array(self.size)/2*cell_size*scale).astype(int)
        if index:
            self.rect = self.image.get_rect(topleft= (self.pos + np.array(self.index)*cell_size*scale))
        self.render(scale=scale)
    
    def render(self, scale=1):
        self.image.fill((0,0,0,0))
        poly = (np.subtract([border_w*scale, (1-inner_prop)/2*cell_size*scale, np.mean([cell_size,inner_prop*cell_size])*scale, (cell_size-border_w)*scale], [1,1,0,0])).astype(int)
        inner = v_gradient(int(inner_prop*cell_size*scale), int(inner_prop*cell_size*scale), self.color[1], self.color[2], trans=self.trans).convert_alpha()
        pygame.draw.rect(self.image, list(self.color[0]) + [self.trans], self.image.get_rect(), poly[0])
        self.image.blit(inner, ((1-inner_prop)/2*cell_size*scale, (1-inner_prop)/2*cell_size*scale))
        
        pygame.draw.polygon(self.image, list(np.clip(np.mean([self.color[1], self.color[2]], axis=0) +70, 0, 255)) + [self.trans], 
                            [(poly[0], poly[0]), (poly[3], poly[0]), (poly[2], poly[1]), (poly[1], poly[1])])
        pygame.draw.polygon(self.image, list(np.clip(np.mean([self.color[1], self.color[2]], axis=0) +10, 0, 255)) + [self.trans], 
                            [(poly[0], poly[0]), (poly[1], poly[1]), (poly[1], poly[2]), (poly[0], poly[3])])
        pygame.draw.polygon(self.image, list(np.clip(np.mean([self.color[1], self.color[2]], axis=0) -40, 0, 255)) + [self.trans], 
                            [(poly[1], poly[2]), (poly[2], poly[2]), (poly[3], poly[3]), (poly[0], poly[3])])
        pygame.draw.polygon(self.image, list(np.clip(np.mean([self.color[1], self.color[2]], axis=0) -10, 0, 255)) + [self.trans], 
                            [(poly[3], poly[0]), (poly[3], poly[3]), (poly[2], poly[2]), (poly[2], poly[1])])
    
    def new_pos(self, pos, scale=1):
        self.pos = pos
        self.scale = scale
        self.image = pygame.Surface((cell_size*scale, cell_size*scale), pygame.SRCALPHA)
        self.center = (np.array(self.pos) + np.array(self.size)/2*cell_size*scale).astype(int)
        if self.board:
            self.rect = self.image.get_rect(topleft=(self.pos))
        else:
            self.rect = self.image.get_rect(topleft= (self.pos + np.array(self.index)*cell_size*scale))
        self.render(scale=scale)
        
    def follow(self, old, new, dist):
        self.pos += np.subtract(new, old)
        self.new_pos(new-dist, scale=self.scale)
    
    def board_convert(self, new_index):
        self.board = True
        self.index = new_index
        self.new_pos(np.add(back_rect.topleft, np.array(new_index)*cell_size))

board = pygame.sprite.Group()
three_center = list(zip(([back_rect.x+back_rect.width/6, back_rect.centerx, back_rect.x+back_rect.width*5/6]),[int(np.mean([screen.get_height(), back_rect.y+back_rect.height]))]*3))
pieces = reset_pieces()
pickup = -1
clear_list = []
game_over = False
score, combo, last_combo = 0, 0, 3
last_score = [score, 0, 0]
show_score = score
board_place = False

def piece_place(pos):
    place = True
    indices = []
    for cell in pieces[pickup]:
        if back_rect.collidepoint(cell.rect.center):
            board_index = None
            for i in range(8):
                for j in range(8):
                    if pygame.Rect(back_rect.x+i*cell_size, back_rect.y+j*cell_size, cell_size, cell_size).collidepoint(cell.rect.center):
                        board_index = [i,j]
                        all_taken = [list(sprite.index) for sprite in board]
                        if board_index not in all_taken:
                            indices.append(board_index)
                        else:
                            place = False
            if not board_index:
                place = False
        else:
            place = False
    return place, indices

def refresh():
    screen.blit(v_gradient(screen.get_width(), screen.get_height(), (57, 83, 149), (95, 128, 205)), (0,0))
    for col in range(8):
        for row in range(8):
            add_rect = pygame.Rect(back_rect.x+col*cell_size, back_rect.y+row*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (36, 44, 84), add_rect)
            pygame.draw.rect(screen, (30, 38, 74), add_rect, border_w)
    outline = pygame.Rect(back_rect.x-offset, back_rect.y-offset, 8*cell_size+2*offset, 8*cell_size+2*offset)
    pygame.draw.rect(screen, (30, 38, 74), outline, offset+border_w)
    board.draw(screen)
    score_text = pygame.font.Font("static/LeagueSpartan-SemiBold.ttf", 72)
    score_surface = score_text.render(str(int(show_score)), True, (255,255,255))
    score_rect = score_surface.get_rect()
    score_rect.center = (screen.get_rect().centerx, back_rect.y/2)
    screen.blit(score_surface, score_rect)
    
    for x in clear_list:
        if x[2]:
            x[0].render()
            screen.blit(x[0].image, x[0].rect)
    for i in range(3):
        pieces[i].draw(screen)
    if game_over:
        no_space_bar = pygame.Rect(0, int(screen.get_height()*(3/4)), screen.get_width(), int(screen.get_height()/6))
        trans = pygame.Surface((no_space_bar.width, no_space_bar.height), pygame.SRCALPHA)
        trans.fill((10,10,10,130))
        screen.blit(trans, no_space_bar.topleft)
        text = pygame.font.Font("static/LeagueSpartan-SemiBold.ttf", 48)
        text_surface = text.render('No Space Left', True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = no_space_bar.center
        screen.blit(text_surface, text_rect)
    if pickup>-1:
        place, indices = piece_place(pygame.mouse.get_pos())
        if place:
            index = [min(x) for x in zip(*indices)]
            for block in pieces[pickup]:
                c = next(key for key,value in block_colors.items() if value==block.color)
                light_copy = Block(np.add(back_rect.topleft, np.array(index)*cell_size + np.array(block.size)*cell_size/2), index=block.index, size=block.size, color=c, trans=100)
                light_copy.render()
                screen.blit(light_copy.image, light_copy.rect)
        pieces[pickup].draw(screen)

refresh()
dist = None
mouse_pos = pygame.mouse.get_pos()
next_delay = 20
disappear_time = 10*next_delay
clear_color = block_colors['black']
board_clear_score = score
score_time = 150

while True:
    events = pygame.event.get()
    current = pygame.time.get_ticks()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
    
    if not game_over:
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                for index,piece in enumerate(pieces):
                    if piece.sprites():
                        first = piece.sprites()[0]
                        hitbox = pygame.Rect(0,0, 5*cell_size*first.scale, 5*cell_size*first.scale)
                        hitbox.center = first.center
                        if hitbox.collidepoint(event.pos):
                            dist = np.subtract(event.pos, first.pos)
                            pickup = index
                            for sprite in piece:
                                sprite.new_pos(first.pos)
                                
            if event.type == MOUSEMOTION:
                if pickup>-1:
                    for sprite in pieces[pickup]:
                        sprite.follow(mouse_pos, event.pos, dist)
                mouse_pos = event.pos
                pieces[pickup].draw(screen)
                
            if event.type == MOUSEBUTTONUP:
                if pickup != -1:
                    place, indices = piece_place(event.pos)
                    if place:
                        place_indices = indices
                        last_score = [score, current, current+score_time]
                        score += len(pieces[pickup])
                        index = [min(x) for x in zip(*indices)]
                        for sprite in pieces[pickup]:
                            sprite.new_pos(np.add(back_rect.topleft,np.array(index)*cell_size))
                        board.add(pieces[pickup].sprites())
                        for i,sprite in enumerate(pieces[pickup]):
                            sprite.board_convert(indices[i])
                        clear_color = pieces[pickup].sprites()[0].color
                        pieces[pickup].empty()
                    else:
                        for sprite in pieces[pickup]:
                            sprite.new_pos((np.array(three_center[pickup]) - np.array(sprite.size)/2*cell_size*start_size).astype(int), scale=start_size)
                    pickup = -1
                
        if not any([(False if len(pieces[i].sprites())==0 else True) for i in range(3)]):
            pieces = reset_pieces()
        clear_row, clear_col = [],[]
        for k in [0,1]:
            for row in range(8):
                check = True
                for col in range(8):
                    index = ([col,row] if bool(k) else [row,col])
                    if index not in [sprite.index for sprite in board]:
                        check = False
                        break
                if check:
                    [clear_row,clear_col][k].append(row)
        
        if clear_row + clear_col:
            clear_total = len(clear_row)+len(clear_col)
            last_score[2] = current + score_time*(clear_total+1)
            temp_add = 10*clear_total
            if clear_total > 1:
                temp_add *= clear_total-1
            if last_combo <= 3:
                combo += clear_total
                score += temp_add*(combo+1)
            else:
                score += temp_add
            last_combo = 0
        else:
            if score>last_score[0]:
                last_combo += 1

        color_key = next(key for key,value in block_colors.items() if value==clear_color)
        if board:
            for k in [0,1]:
                for sprite in board.sprites():
                    if sprite.index[k] in [clear_row,clear_col][k]:
                        show = False
                        time = disappear_time + current
                        if sprite.index[k^1]==0 and [clear_row,clear_col][k].index(sprite.index[k])==0:
                            show = True
                        else:
                            time = next_delay*sprite.index[k^1] + 5*[clear_row,clear_col][k].index(sprite.index[k])*next_delay + current
                        clear_list.append([Block(np.array(back_rect.topleft) + np.full((2), cell_size/2), (1,1), index=sprite.index, color=color_key), time, show])
                        board.remove(sprite)
        else:
            if score>board_clear_score:
                score += 300
                last_score[2] = current + score_time*8
                board_clear_score = score
                clear_list = []
                for i in range(8):
                    for j in range(8):
                        show = False
                        time = disappear_time + current
                        if [i,j]==[0,0]:
                            show = True
                        else:
                            time = next_delay*(i+j)*(3/2) + current
                        c = np.random.choice(['red','orange','yellow','green','light_blue','dark_blue','purple'])
                        clear_list.append([Block(np.array(back_rect.topleft) + np.full((2), cell_size/2), (1,1), index=[i,j], color=c), time, show])

        found = [False]*len(pieces)
        for i,piece in enumerate(pieces):
            found[i] = can_place(piece)
        if not any(found):
            game_over = True
            for row in range(8):
                for col in range(8):
                    if [col,row] not in [sprite.index for sprite in board]:
                        show = False
                        time = disappear_time + current
                        if row==7:
                            show = True
                        else:
                            time = (7-row)*3*next_delay + current
                        clear_list.append([Block(np.array(back_rect.topleft) + np.full((2), cell_size/2), (1,1), index=[col,row], color='no_space'), time, show])
    
    if clear_list:
        expired = []
        for i,x in enumerate(clear_list):
            if x[2]:
                if x[1]<=current:
                    if game_over:
                        if next(key for key,value in block_colors.items() if value==block_colors['no_space']):
                            x[1] = math.inf
                        else:
                            expired.append(x)
                    else:
                        expired.append(x)
                else:
                    if game_over and x[1]<math.inf:
                        ratio = (1 - (x[1]-current) / (disappear_time))
                        x[0].trans = ratio * 255
                        save_index = x[0].index
                        x[0].index = [0,0]
                        x[0].new_pos(np.array(back_rect.topleft) + np.full((2), cell_size) * ((1-ratio)/2 + np.array(save_index)), scale=ratio)
                        x[0].index = save_index
                    elif game_over:
                        x[0].trans = 255
                        x[0].new_pos(np.array(back_rect.topleft))
            else:
                if x[1]<=current:
                    x[2] = True
                    x[1] = disappear_time + current
                    if game_over:
                        x[0].trans = 0
        for x in expired:
            clear_list.remove(x)
    
    if show_score < score:
        show_score = last_score[0] + (score - last_score[0]) * (current - last_score[1]) / (last_score[2] - last_score[1])
    else:
        last_score[0] = score
    
    refresh()
    pygame.display.flip()