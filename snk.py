import pygame as pg
import random
import os, sys
from vars import *
pg.init()
pg.font.init()

pg.display.set_icon(pg.image.load(os.path.join(images_path,'big_0.png')))

class Button:
    def __init__(self, x, y, width, height, font, text_color=(0, 0, 0), color=(0, 0, 0), text="", font_size = 30):
        self.x = int(k * x)
        self.y = int(k * y)
        self.width = int(k * width)
        self.height = int(k * height)
        self.font = pg.font.Font(os.path.join(font_path, font), int(k*font_size))
        self.color = color
        self.text = text
        self.text_color = text_color
        
    def draw(self):
        if self.color != (0, 0, 0):
            pg.draw.rect(display, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != "":
            lines = self.text.split("\n")
            for i, line in enumerate(lines, start=1):
                text = self.font.render(line, True, self.text_color)

                display.blit(
                    text,
                    (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/(len(lines) + 1) * i - text.get_height()/2))
                    )

    def is_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

class PictureButton:
    def __init__(self, x, y, width, height, picture):
        self.x = int(k * x)
        self.y = int(k * y)
        self.width = int(k * width)
        self.height = int(k * height)
        self.picture = picture
        
    def draw(self):
        display.blit(pg.transform.scale(self.picture, (self.width, self.height)), (self.x, self.y))
        
    def is_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False





### кнопки
menu_button = Button(635, 30, 130, 45, "sc bold.ttf", text="MENU", font_size = 60)
speed_button = Button(650, 100, 100, 30, "sc bold.ttf", text="Speed", font_size = 40)
up_button = Button(655, 135, 25, 25, "sc bold.ttf", text = "up", font_size = 20, text_color = (255, 0, 0))
down_button = Button(700, 135, 45, 25, "sc bold.ttf", text = "down", font_size = 20, text_color = (0, 0, 255))
play_button = Button(525, 40, 135, 55, "sc bold.ttf", text = "Play", font_size = 70)
settings_button = Button(462.5, 105, 260, 55, "sc bold.ttf", text = "Settings", font_size = 70)
left_switch_button = Button(660, 165, 30, 30, "sans italic.ttf", text = "<", font_size = 50)
right_switch_button = Button(725, 165, 30, 30, "sans italic.ttf", text = ">", font_size = 50)
switch_number_button = Button(697.5, 165, 20, 30, "sans.ttf", text = str(switch_number), font_size = 40)
back_button = Button(660, 20, 105, 40, "sans italic.ttf", text = "Back", font_size = 50)
save_button = Button(665, 80, 100, 40, "sans italic.ttf", text = "Save", font_size = 50)
eraser_button = PictureButton(665, 210, 90, 60, pg.image.load(os.path.join(images_path, "eraser.png")))
for i in range(1, 12): snake_parts[i] = PictureButton(-4*size/5 + i*(50+5), 25, 50, 50, pg.image.load(os.path.join(images_path, "big_" + str(i) + ".png")))
face_button = PictureButton(cell_coords[0] + 3*65, cell_coords[1] + 3*65, 64, 64, pg.image.load(os.path.join(images_path, "big_0.png")))

### картинки       
surface = pg.transform.scale(pg.image.load(os.path.join(images_path, 'surface.png')), (X, Y))
menu = pg.transform.scale(pg.image.load(os.path.join(images_path, 'menu.png')), (X, Y))
settings = pg.transform.scale(pg.image.load(os.path.join(images_path, 'settings.png')), (X, Y))


### функции
def reset_fight():
    global moves, config, cps, dont_move, spd

    moves = []
    dont_move = [False]*4
    config = []
    spd = spd0
    
    for i in range(amount):
        moves.append([])
    for j in range(length):
        moves[0].append([9*size, 0])
        if amount > 1:moves[1].append([0, 9*size])
        if amount > 2:moves[2].append([9*size, 18*size])
        if amount > 3:moves[3].append([18*size, 9*size])
        
    for i in range(19):
        config.append([0]*19)

    
def move(x, y, direction, i):
    global dont_move

    if not(1 <= x//size and config[y//size][x//size-1] in (0, 3) and [x - size, y] != moves[i][-2]) and not(
           x//size < 18 and config[y//size][x//size+1] in (0, 3) and [x + size, y] != moves[i][-2]) and not(
           1 <= y//size and config[y//size-1][x//size] in (0, 3) and [x, y - size] != moves[i][-2]) and not(
           y//size < 18 and config[y//size+1][x//size] in (0, 3) and [x, y + size] != moves[i][-2]):
        dont_move[i] = True

        
            
    else:
        dont_move[i] = False
    
        if 1 <= x//size and config[y//size][x//size-1] in (0, 3) and direction == 'left' and [x - size, y] != moves[i][-2]:
            x -= size
            changing_coords(x, y, i)
        elif x//size < 18 and config[y//size][x//size+1] in (0, 3) and direction == 'right' and [x + size, y] != moves[i][-2]:
            x += size
            changing_coords(x, y, i)
        elif 1 <= y//size and config[y//size-1][x//size] in (0, 3) and direction == 'up' and [x, y - size] != moves[i][-2]:
            y -= size
            changing_coords(x, y, i)
        elif y//size < 18 and config[y//size+1][x//size] in (0, 3) and direction == 'down' and [x, y + size] != moves[i][-2]:
            y += size
            changing_coords(x, y, i)
        else:
            move(x, y, random.choice(('left', 'right', 'up', 'down')), i)

def changing_coords(x, y, i ):
    global moves, config

    config[moves[i][-2][1] // size][moves[i][-2][0] // size] = 0  
    moves[i] = [[x, y]] + moves[i][:-1]
    
  
    config[moves[i][1][1] // size][moves[i][1][0] // size] = 1
    config[y//size][x//size] = 2
    config[moves[i][-2][1] // size][moves[i][-2][0] // size] = 3


def Quit_the_game():
    global Run, Fight
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            Run = False
            pg.quit()


def head_rotation(i, head_name):
    head = pg.transform.scale(pg.image.load(os.path.join(images_path, head_name)),(size, size))

    if moves[i][0][1] < moves[i][1][1] or moves[i][0] == moves[i][1] == [9*size, 18*size]:
        display.blit(head, moves[i][0])
    if moves[i][0][1] > moves[i][1][1] or moves[i][0] == moves[i][1] == [9*size, 0]:
        display.blit(pg.transform.rotate(head, 180), moves[i][0])
    if moves[i][0][0] > moves[i][1][0] or moves[i][0] == moves[i][1] == [0, 9*size]:
        display.blit(pg.transform.rotate(head, 270), moves[i][0])
    if moves[i][0][0] < moves[i][1][0] or moves[i][0] == moves[i][1] == [18*size, 9*size]:
        display.blit(pg.transform.rotate(head, 90), moves[i][0])


def body_rotation(k, i, head_name, body_name, bodyr_name, bodyl_name, tail_name):
    n = pg.transform.scale(pg.image.load(os.path.join(images_path, body_name)),(size, size))
    l = pg.transform.scale(pg.image.load(os.path.join(images_path, bodyl_name)),(size, size))
    r = pg.transform.scale(pg.image.load(os.path.join(images_path, bodyr_name)),(size, size))

    if moves[i][k][0] > moves[i][k-1][0] and moves[i][k][1] < moves[i][k+1][1]:
        display.blit(l, moves[i][k])
    elif moves[i][k][0] < moves[i][k-1][0] and moves[i][k][1] < moves[i][k+1][1]:
        display.blit(r, moves[i][k])
    elif moves[i][k][0] > moves[i][k-1][0] and moves[i][k][1] > moves[i][k+1][1]:
        display.blit(pg.transform.rotate(r, 180), moves[i][k])
    elif moves[i][k][0] < moves[i][k-1][0] and moves[i][k][1] > moves[i][k+1][1]:
        display.blit(pg.transform.rotate(l, 180), moves[i][k])

    elif moves[i][k][1] > moves[i][k-1][1] and moves[i][k][0] < moves[i][k+1][0]:
        display.blit(pg.transform.rotate(r, 90), moves[i][k])
    elif moves[i][k][1] < moves[i][k-1][1] and moves[i][k][0] < moves[i][k+1][0]:
        display.blit(pg.transform.rotate(l, 90), moves[i][k])
    elif moves[i][k][1] > moves[i][k-1][1] and moves[i][k][0] > moves[i][k+1][0]:
        display.blit(pg.transform.rotate(l, 270), moves[i][k])
    elif moves[i][k][1] < moves[i][k-1][1] and moves[i][k][0] > moves[i][k+1][0]:
        display.blit(pg.transform.rotate(r, 270), moves[i][k])
    else:
        if moves[i][k][0] == moves[i][k-1][0]:
            if moves[i][k][1] > moves[i][k-1][1]:
                display.blit(n, moves[i][k])
            else:
                display.blit(pg.transform.rotate(n, 180), moves[i][k])
        else:
            if moves[i][k][0] > moves[i][k-1][0]:
                display.blit(pg.transform.rotate(n, 90), moves[i][k])
            else:
                display.blit(pg.transform.rotate(n, 270), moves[i][k])


def tail_rotation(i, tail_name):
    tail = pg.transform.scale(pg.image.load(os.path.join(images_path, tail_name)),(size, size))
    if moves[i][-2] == moves[i][-3]: f = 4
    else: f = 3
    
    if moves[i][-2][1] > moves[i][-f][1]:
        display.blit(tail,(moves[i][-2][0], moves[i][-2][1]))
    else:
        if moves[i][-2][0] > moves[i][-f][0]:
            display.blit(pg.transform.rotate(tail, 90),(moves[i][-2][0], moves[i][-2][1]))
        if moves[i][-2][0] < moves[i][-f][0]:
            display.blit(pg.transform.rotate(tail, 270),(moves[i][-2][0], moves[i][-2][1]))
        if moves[i][-2][1] < moves[i][-f][1]:
            display.blit(pg.transform.rotate(tail, 180),(moves[i][-2][0], moves[i][-2][1]))



def prints(i, head_name, body_name, bodyr_name, bodyl_name, tail_name):
    head_rotation(i, head_name)

    if len(moves[i]) > 2:
        for k in range(1, len(moves[i]) - 2):
            if not moves[i][k-1] == moves[i][k]:
                body_rotation(k, i, head_name, body_name, bodyr_name, bodyl_name, tail_name)

    tail_rotation(i, tail_name)

def menu_buttons():
    global Menu, Fight, Settings, spd
    play_button.draw()
    settings_button.draw()
    if play_button.is_over(mouse_pos) or settings_button.is_over(mouse_pos):
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
    else:
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
        
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            
            if play_button.is_over(mouse_pos):
                Menu = False
                Fight = True
                reset_fight()
                
            elif settings_button.is_over(mouse_pos):
                Settings = True
                for i in range(amount):
                    creating_new_comand(i)
                Menu = False


def fight_buttons():
    global Fight, Menu, spd
    
    speed_button.draw(), menu_button.draw(), up_button.draw(), down_button.draw()
    
    if menu_button.is_over(mouse_pos) or up_button.is_over(mouse_pos) or down_button.is_over(mouse_pos):
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
    else:
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
        
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if up_button.is_over(mouse_pos) and spd <= 100:
                spd += 5
            elif down_button.is_over(mouse_pos) and spd >= 3:
                spd -= 5
            elif menu_button.is_over(mouse_pos):
                Fight = False
                Menu = True

def settings_buttons():
    global switch_number, Settings, Menu, eraser_button, face_button, face_spin
 
    if event.type == pg.MOUSEBUTTONDOWN:
        if eraser_button.is_over(mouse_pos) and eraser_button.width != 105:
            eraser_button = PictureButton(657.5, 205, 105, 70, pg.image.load(os.path.join(images_path, "eraser.png")))
        else:
            eraser_button = PictureButton(665, 210, 90, 60, pg.image.load(os.path.join(images_path, "eraser.png")))
                
            if left_switch_button.is_over(mouse_pos):
                if switch_number > 1:
                    switch_number -= 1
                else:
                    switch_number = 4
            elif right_switch_button.is_over(mouse_pos):
                if switch_number < 4:
                    switch_number += 1
                else:
                    switch_number = 1
            elif back_button.is_over(mouse_pos):
                face_spin = 0
                Settings = False
                Menu = True
                        
                for i in range(1, 12):
                    snake_parts[i].picture = pg.image.load(os.path.join(images_path, "big_" + str(i) + ".png"))
            elif face_button.is_over(mouse_pos):
                face_spin += 90
            elif save_button.is_over(mouse_pos):
                saving()

def draw_settings_buttons():
    global switch_number_button
    
    switch_number_button.text = str(switch_number)
    face_button.picture = pg.transform.rotate(pg.image.load(os.path.join(images_path, "big_0.png")), -face_spin)

    left_switch_button.draw(), right_switch_button.draw(), switch_number_button.draw(), back_button.draw(), eraser_button.draw(), save_button.draw(), face_button.draw()
    for i in range(1, 12):
        snake_parts[i].draw()

    
    if (left_switch_button.is_over(mouse_pos) or right_switch_button.is_over(mouse_pos)
        or back_button.is_over(mouse_pos) or save_button.is_over(mouse_pos)
        or eraser_button.is_over(mouse_pos) or face_button.is_over(mouse_pos)):
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
    else:
        for i in range(1, 12):
            if snake_parts[i].is_over(mouse_pos):
                pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
                break
            if i == 10:
                pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
        
def snake_parts_registration():
    global snake_parts, spin, Settings, Menu, grabbed
    
    if event.type == pg.MOUSEWHEEL:
        for i in range(1, 12):
            if grabbed[i]:
                snake_parts[i].picture = pg.transform.rotate(snake_parts[i].picture, 90*event.y)
                spin += 90*event.y
                break
                        
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:


        if eraser_button.width == int(k*105):
            release_registration(-1)
            
        for i in range(1, 12):

            if grabbed[i]:
                release_registration(i)
                snake_parts[i] = PictureButton(-4*size/5 + i*(50+5), 25, 50, 50, snake_parts[i].picture)
                grabbed[i] = False
                break
            if not grabbed[i]:
                if snake_parts[i].is_over(mouse_pos):
                    snake_parts[i] = PictureButton(-4*(size+4)/5 + i*(50+5), 21, 58, 58, snake_parts[i].picture)
                    grabbed[i] = True


def release_registration(i):
    global new_comand, spins, spin, snakes_parts
    x, y = int((mouse_pos[0]-k*cell_coords[0])//(k*64)), int((mouse_pos[1]-k*cell_coords[1])//(k*64))
    if 0 <= x <= 6 and 0 <= y <= 6:
        new_comand[switch_number-1][y][x] = i
        if i != -1:
            spins[switch_number-1][y][x] = pg.transform.scale(snake_parts[i].picture, (int(k*64), int(k*64)))
            spin = 0
            snake_parts[i].picture = pg.image.load(os.path.join(images_path, 'big_' + str(i) + '.png'))


def creating_new_comand(I):
    global new_comand
    new_comand[I] = []
    for i in range(7):
        new_comand[I].append([-1, -1, -1, -1, -1, -1, -1])

def blitting_of_released():
    for i in range(7):
        for j in range(7):
            if new_comand[switch_number-1][i][j] != -1 and not(i == j == 3) and new_comand[switch_number-1][i][j] != 0:
                display.blit(spins[switch_number-1][i][j], (k*cell_coords[0] + j*64.4*k + j, k*cell_coords[1] + i*64.4*k + i))


def saving():
    global snakes_data, new_comand
    for i in range(face_spin // 90): #возвращает команду в положение, при котором голова направлена вверх
        new_comand[switch_number-1] = rotate_mas(new_comand[switch_number-1])

    for i in range(7):
        for j in range(7):
            
            if new_comand[switch_number-1][i][j] == 11:
                new_comand[switch_number-1][i][j] = 'fr'   
            elif new_comand[switch_number-1][i][j] == 10:
                new_comand[switch_number-1][i][j] = 'st'
                
            elif new_comand[switch_number-1][i][j] == 9:
                new_comand[switch_number-1][i][j] = 't2'
            elif 6 <= new_comand[switch_number-1][i][j] <= 8:
                new_comand[switch_number-1][i][j] = 'b2'
            elif new_comand[switch_number-1][i][j] == 5:
                new_comand[switch_number-1][i][j] = 'h2'
            
                
            elif new_comand[switch_number-1][i][j] == 4:
                new_comand[switch_number-1][i][j] = 't1'
            elif 1 <= new_comand[switch_number-1][i][j] <= 3:
                new_comand[switch_number-1][i][j] = 'b1'
            elif new_comand[switch_number-1][i][j] == 0:
                new_comand[switch_number-1][i][j] = 'h1'
                
            elif new_comand[switch_number-1][i][j] == -1:
                new_comand[switch_number-1][i][j] = 'nt'
        
    snakes_data[switch_number-1].append(new_comand[switch_number-1])
    creating_new_comand(switch_number-1)
    
    print(snakes_data[switch_number-1])
    print()


def analysis(I):
    global region, config
    x, y = int(moves[I][0][0]//size) - 3, int(moves[I][0][1]//size) - 3
    region[I] = []

    for i in range(7):
        region[I].append(['fr', 'fr', 'fr', 'fr', 'fr', 'fr', 'fr'])

    for i in range(7):
        for j in range(7):
            if 0 <= y+i <= 18 and 0 <= x+j <= 18:
                if config[y+i][x+j] == 2:
                    if i == j == 3:
                        region[I][i][j] = 'h1'
                    else:
                        region[I][i][j] = 'h2'

                elif config[y+i][x+j] == 1:
                    region[I][i][j] = 'b1'
                    for k in range(amount):
                        for l in range(1, len(moves[k])-2):
                            if k != I and moves[k][l][0] == size*(x+j) and moves[k][l][1] == size*(y+i):
                                region[I][i][j] = 'b2'
                                break
                                
                elif config[y+i][x+j] == 3:
                    region[I][i][j] = 't1'
                    for k in range(amount):
                        if k != I and moves[k][-2][0] == size*(x+j) and moves[k][-2][1] == size*(y+i):
                            region[I][i][j] = 't2'
                            break
                            
            else:
                if ((y+i == -1 or y+i == 19) and (-1 <= x+j <= 19)) or ((x+j == -1 or x+j == 19) and (-1 <= y+i <= 19)):
                    region[I][i][j] = 'st'
                else:
                    region[I][i][j] = 'ed'
    
def rotate_mas(mas):
    rotated_mas = [[], [], [], [], [], [], []]

    for i in range(7):
        for j in range(7):
            rotated_mas[i].append(mas[i][j])
        
    for j in range(7):
        for i in range(6, -1, -1):
            rotated_mas[i][j] = mas[j][6-i]
    return rotated_mas


def print_snake(I):
    global equil
    equil = False
    check_bite()
    if not dont_move[i]:
        for comand in snakes_data[I]:
            comparing(comand, region[I], I, 0)
            if equil: break
            
    if not(equil):
        move(moves[I][0][0], moves[I][0][1], random.choice(['up', 'down', 'left', 'right']), I)

    


def comparing(comand, region, I, num_of_direct):
    global equil
    equil = True
    
    for i in range(7):
        for j in range(7):
            if comand[i][j] != region[i][j] and comand[i][j] != 'nt':
                equil = False
                break
    if equil:
        move(moves[I][0][0], moves[I][0][1], ['up', 'left', 'down', 'right'][num_of_direct], I)
                
    elif num_of_direct != 3:
        comparing(rotate_mas(comand), region, I, num_of_direct + 1)


def check_bite():
    global moves, config, spd 
    for i in range(amount):
        for j in range(amount):
            if moves[i][0][0] == moves[j][-2][0] and moves[i][0][1] == moves[j][-2][1]:

                config[moves[i][-2][1]//size][moves[i][-2][0]//size] = 2
                moves[i].append([moves[i][-1][0], moves[i][-1][1]])
                moves[j] = moves[j][:-1]
                
                if len(moves[j]) > 3:
                    config[moves[j][-2][1]//size][moves[j][-2][0]//size] = 3


while Run:
    clock.tick(spd)
    mouse_pos = pg.mouse.get_pos()
    if Fight: 
        display.blit(surface, (0, 0))

        fight_buttons()
        for i in range(amount):
            prints(i, 'head' + str(i+1) + '.png', 'body' + str(i+1) + '.png', 'body' + str(i+1) + '_right.png', 'body' + str(i+1) + '_left.png', 'tail' + str(i+1) + '.png')
            
            if len(moves[i]) > 3:
##                if not dont_move[0] + dont_move[1] + dont_move[2] + dont_move[3] == 3:
                analysis(i)
                print_snake(i)
                    
            else:
                dont_move[i] = True
                config[moves[i][-2][1]//size][moves[i][-2][0]//size] = 4
    
    if Menu:
        spd = 60

        display.blit(menu, (0, 0))

        menu_buttons()

    if Settings:
        spd = 60
        
        display.blit(settings, (0, 0))
        display.blit(pg.transform.scale(pg.image.load(os.path.join(images_path, "cell.png")), (int(k*454), int(k*454))), (k*cell_coords[0], k*cell_coords[1]))
        
        draw_settings_buttons()
            
        for event in pg.event.get():
            snake_parts_registration()
            settings_buttons()
            
        blitting_of_released()
        


    pg.display.update()
    Quit_the_game()
