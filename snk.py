import pygame as pg
import random
import os, sys

pg.init()
pg.font.init()

class Button:
    def __init__(self, x, y, width, height, font, text_color=(0, 0, 0), color=(0, 0, 0), text="", font_size = 30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pg.font.Font(os.path.join(font_path, font), font_size)
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = picture
        
    def draw(self):
        display.blit(pg.transform.scale(self.picture, (self.width, self.height)), (self.x, self.y))
        
    def is_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

# переменные
X, Y = 800, 600
size = Y // 20

current_path = os.path.dirname(__file__)
resources_path = os.path.join(current_path, 'resources')
font_path = os.path.join(resources_path, 'fonts')
images_path = os.path.join(resources_path, 'images')

clock = pg.time.Clock()
display = pg.display.set_mode((X, Y))
keys = pg.key.get_pressed()
pg.display.set_icon(pg.image.load(images_path + '\\big_0.png'))

Run = True
Menu = True
Fight = False
Settings = False

new_comand = [[], [], [], []]
spins = [[], [], [], []]
for j in range(4):
    for i in range(7):
        spins[j].append([0, 0, 0, 0, 0, 0, 0])
switch_number = 1
grabbed = [False] * 11
region = [[], [], [], []]
spin = 0
spd = 30
snake_parts = [0]*11
cell_coords = (73, 145)

snakes_data = [
[
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'st', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'b1', 'st', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['st', 'b1', 'b1', 'h1', 'nt', 'nt', 'nt'], ['nt', 'st', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'nt', 'nt', 'nt'], ['st', 'b1', 'b1', 'b1', 'nt', 'nt', 'nt'], ['nt', 'st', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'st', 'nt', 'nt', 'nt', 'nt', 'nt'], ['st', 'b1', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'b1', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'b1', 'b1', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'st', 'nt', 'nt', 'nt', 'nt', 'nt'], ['st', 'b1', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'b1', 'nt', 'h1', 'nt', 'nt', 'nt'], ['nt', 'b1', 'b1', 'b1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'b1', 'b1', 't1', 'st', 'nt', 'nt'], ['nt', 'b1', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'b1', 'b1', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'b1', 't1', 'nt', 'st', 'nt', 'nt'], ['nt', 'b1', 'nt', 'h1', 'nt', 'nt', 'nt'], ['nt', 'b1', 'b1', 'b1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'st', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'st', 'b1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'b1', 'b1', 'st'], ['nt', 'nt', 'nt', 'nt', 'nt', 'st', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'h1', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'b1', 'b1', 'b1', 'st'], ['nt', 'nt', 'nt', 'nt', 'nt', 'st', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'st', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'b1', 'st'], ['nt', 'nt', 'nt', 'nt', 'nt', 'b1', 'nt'], ['nt', 'nt', 'nt', 'h1', 'b1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'st', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'b1', 'st'], ['nt', 'nt', 'nt', 'h1', 'nt', 'b1', 'nt'], ['nt', 'nt', 'nt', 'b1', 'b1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'st', 't1', 'b1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'b1', 'nt'], ['nt', 'nt', 'nt', 'h1', 'b1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']], 
[['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'st', 'nt', 'nt', 'nt'], ['nt', 'nt', 'st', 'nt', 't1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'h1', 'nt', 'b1', 'nt'], ['nt', 'nt', 'nt', 'b1', 'b1', 'b1', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt'], ['nt', 'nt', 'nt', 'nt', 'nt', 'nt', 'nt']]
],

[
], [], []]



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
eraser_button = PictureButton(665, 210, 90, 60, pg.image.load(images_path + "\\eraser.png"))
for i in range(1, 11): snake_parts[i] = PictureButton(-30 + i*(50+5), 25, 50, 50, pg.image.load(images_path + "\\big_" + str(i) + ".png"))
##№ картинки
        
surface = pg.image.load(images_path + '\\surface.png')
menu = pg.transform.scale(pg.image.load(images_path + '\\menu.png'), (800, 600))
settings = pg.image.load(images_path +'\\settings.png')


### функции

def reset_fight():
    global moves, config, cps, lx, ly, shadows, shadow_coords, dont_move, spd

    moves = []
    shadow_coords = []
    lx, ly = 0, 0
    shadows = []
    dont_move = [False]*8
    config = []
    spd = 10

    for i in range(4):
        moves.append([])
        for j in range(7):
            moves[i].append([0, -100])

    for i in range(20):
        config.append([0]*20)

    for i in range(4):
        shadows.append([])
        for j in range(7):
            shadows[i].append([0, 0])

    for i in range(4):
        shadow_coords.append([0, 0])

    moves[0][0][0] = 570; moves[0][0][1] = 0
    moves[1][0][0] = 0; moves[1][0][1] = 570
    moves[2][0][0] = 0; moves[2][0][1] = 0
    moves[3][0][0] = 570; moves[3][0][1] = 570


def move(x, y, direction, i):
    global dont_move, lx, ly

    if not(1 <= x//30 and config[y//30][x//30-1] == 0) and not(x//30 < 19 and config[y//30][x//30+1] == 0) and not(1 <= y//30 and config[y//30-1][x//30] == 0) and not(y//30 < 19 and config[y//30+1][x//30] == 0):
        dont_move[i] = True
            
    else:
        dont_move[i] = False
        lx, ly = x, y

    
        if 1 <= x//30 and config[y//30][x//30-1] == 0 and direction == 'left':
            lx -= size
            dont_move[i] = False
        elif x//30 < 19 and config[y//30][x//30+1] == 0 and direction == 'right':
            lx += size
            dont_move[i] = False
        elif 1 <= y//30 and config[y//30-1][x//30] == 0 and direction == 'up':
            ly -= size
            dont_move[i] = False
        elif y//30 < 19 and config[y//30+1][x//30] == 0 and direction == 'down':
            ly += size
            dont_move[i] = False
        else:
            move(x, y, random.choice(('left', 'right', 'up', 'down')), i)

def restore():
    global moves, lx, ly
    for i in range(8):
        if dont_move[i]:
            for j in range(len(shadows[i])):
                moves[i][j] = shadows[i][j]
            lx = shadow_coords[i][0]
            ly = shadow_coords[i][1]
            for j in range(7):
                if j == 0:
                    config[moves[i][j][1]//30][moves[i][j][0]//30] = 2
                else:
                    config[moves[i][j][1]//30][moves[i][j][0]//30] = 1


def changing_coords(i):
    global moves, config
    config[moves[i][6][1] // 30][moves[i][6][0] // 30] = 0

    for j in range(len(moves[i])-1, 0, -1):
        moves[i][j][0] = moves[i][j-1][0]
        moves[i][j][1] = moves[i][j-1][1]
        config[moves[i][j][1] // 30][moves[i][j][0] // 30] = 1

    moves[i][0][0], moves[i][0][1] = lx, ly
    config[ly//30][lx//30] = 2
    config[moves[i][6][1] // 30][moves[i][6][0] // 30] = 3


def Quit_the_game():
    global Run, Fight
    for event in pg.event.get():
        if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
            Run = False
            pg.quit()


def head_rotation(i, head_name):
    head = pg.transform.scale(pg.image.load(images_path + "\\" + head_name),(size, size))

    if moves[i][0][1] < moves[i][1][1]:
        display.blit(head, (moves[i][0][0], moves[i][0][1]))
    if moves[i][0][1] > moves[i][1][1]:
        display.blit(pg.transform.rotate(head, 180), (moves[i][0][0], moves[i][0][1]))
    if moves[i][0][0] > moves[i][1][0]:
        display.blit(pg.transform.rotate(head, 270), (moves[i][0][0], moves[i][0][1]))
    if moves[i][0][0] < moves[i][1][0]:
        display.blit(pg.transform.rotate(head, 90), (moves[i][0][0], moves[i][0][1]))


def body_rotation(k, i, head_name, body_name, bodyr_name, bodyl_name, tail_name):
    n = pg.transform.scale(pg.image.load(images_path + "\\" + body_name),(size, size))
    l = pg.transform.scale(pg.image.load(images_path + "\\" + bodyl_name),(size, size))
    r = pg.transform.scale(pg.image.load(images_path + "\\" + bodyr_name),(size, size))

    if moves[i][k][0] > moves[i][k-1][0] and moves[i][k][1] < moves[i][k+1][1]:
        display.blit(l,(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][0] < moves[i][k-1][0] and moves[i][k][1] < moves[i][k+1][1]:
        display.blit(r,(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][0] > moves[i][k-1][0] and moves[i][k][1] > moves[i][k+1][1]:
        display.blit(pg.transform.rotate(r, 180),(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][0] < moves[i][k-1][0] and moves[i][k][1] > moves[i][k+1][1]:
        display.blit(pg.transform.rotate(l, 180),(moves[i][k][0], moves[i][k][1]))

    elif moves[i][k][1] > moves[i][k-1][1] and moves[i][k][0] < moves[i][k+1][0]:
        display.blit(pg.transform.rotate(r, 90),(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][1] < moves[i][k-1][1] and moves[i][k][0] < moves[i][k+1][0]:
        display.blit(pg.transform.rotate(l, 90),(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][1] > moves[i][k-1][1] and moves[i][k][0] > moves[i][k+1][0]:
        display.blit(pg.transform.rotate(l, 270),(moves[i][k][0], moves[i][k][1]))
    elif moves[i][k][1] < moves[i][k-1][1] and moves[i][k][0] > moves[i][k+1][0]:
        display.blit(pg.transform.rotate(r, 270),(moves[i][k][0], moves[i][k][1]))
    else:
        if moves[i][k][0] == moves[i][k-1][0]:
            if moves[i][k][1] > moves[i][k-1][1]:
                display.blit(n,(moves[i][k][0], moves[i][k][1]))
            else:
                display.blit(pg.transform.rotate(n, 180),(moves[i][k][0], moves[i][k][1]))
        else:
            if moves[i][k][0] > moves[i][k-1][0]:
                display.blit(pg.transform.rotate(n, 90),(moves[i][k][0], moves[i][k][1]))
            else:
                display.blit(pg.transform.rotate(n, 270),(moves[i][k][0], moves[i][k][1]))


def tail_rotation(i, tail_name):
    tail = pg.transform.scale(pg.image.load(images_path + "\\" + tail_name),(size, size))

    if moves[i][6][1] > moves[i][5][1]:
        display.blit(tail,(moves[i][6][0], moves[i][6][1]))
    else:
        if moves[i][6][0] > moves[i][5][0]:
            display.blit(pg.transform.rotate(tail, 90),(moves[i][6][0], moves[i][6][1]))
        if moves[i][6][0] < moves[i][5][0]:
            display.blit(pg.transform.rotate(tail, 270),(moves[i][6][0], moves[i][6][1]))
        if moves[i][6][1] < moves[i][5][1]:
            display.blit(pg.transform.rotate(tail, 180),(moves[i][6][0], moves[i][6][1]))


def prints(i, head_name, body_name, bodyr_name, bodyl_name, tail_name):
    head_rotation(i, head_name)

    for k in range(1, 6):
        body_rotation(k, i, head_name, body_name, bodyr_name, bodyl_name, tail_name)

    tail_rotation(i, tail_name)


def remember(i):
    global shadows, shadow_coords
    for k in range(len(moves[i])):
        for j in range(2):
            shadows[i][k][j] = moves[i][k][j]
    shadow_coords[i][0], shadow_coords[i][1] = lx, ly




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
                for i in range(4):
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
            if up_button.is_over(mouse_pos) and spd <= 30:
                spd += 3
            elif down_button.is_over(mouse_pos) and spd >= 3:
                spd -= 3
            elif menu_button.is_over(mouse_pos):
                Fight = False
                Menu = True

def settings_buttons():
    global switch_number, Settings, Menu, eraser_button
 
    if event.type == pg.MOUSEBUTTONDOWN:
        if eraser_button.is_over(mouse_pos) and eraser_button.width != 105:
            eraser_button = PictureButton(657.5, 205, 105, 70, pg.image.load(images_path + "\\eraser.png"))
        else:
            eraser_button = PictureButton(665, 210, 90, 60, pg.image.load(images_path + "\\eraser.png"))
                
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
                Settings = False
                Menu = True
            elif save_button.is_over(mouse_pos):
                saving()

def draw_settings_buttons():
    global switch_number_button
    
    switch_number_button.text = str(switch_number)
    
    left_switch_button.draw(), right_switch_button.draw(), switch_number_button.draw(), back_button.draw(), eraser_button.draw(), save_button.draw()
    for i in range(1, 11):
        snake_parts[i].draw()

    
    if left_switch_button.is_over(mouse_pos) or right_switch_button.is_over(mouse_pos) or back_button.is_over(mouse_pos) or save_button.is_over(mouse_pos) or eraser_button.is_over(mouse_pos):
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
    else:
        for i in range(1, 11):
            if snake_parts[i].is_over(mouse_pos):
                pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
                break
            if i == 10:
                pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
        
def snake_parts_registration():
    global snake_parts, spin, Settings, Menu, grabbed
    
    if event.type == pg.MOUSEWHEEL:
        for i in range(1, 11):
            if grabbed[i]:
                snake_parts[i].picture = pg.transform.rotate(snake_parts[i].picture, 90*event.y)
                spin += 90*event.y
                break
                        
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

        if back_button.is_over(mouse_pos): # выход в меню
            Settings = False
            Menu = True
                    
            for i in range(1, 11):
                snake_parts[i].picture = pg.image.load(images_path + "\\big_" + str(i) + ".png")

        if eraser_button.width == 105:
            release_registration(-1)

        for i in range(1, 11):

            if grabbed[i]:
                release_registration(i)
                snake_parts[i] = PictureButton(-30 + i*(50+5), 25, 50, 50, snake_parts[i].picture)
                grabbed[i] = False
                break
            if not grabbed[i]:
                if snake_parts[i].is_over(mouse_pos):
                    snake_parts[i] = PictureButton(-34 + i*(50+5), 21, 58, 58, snake_parts[i].picture)
                    grabbed[i] = True


def release_registration(i):
    global new_comand, spins, spin, snakes_parts
    x, y = int((mouse_pos[0]-cell_coords[0])//64), int((mouse_pos[1]-cell_coords[1])//64)
    if 0 <= x <= 6 and 0 <= y <= 6:
        new_comand[switch_number-1][y][x] = i
        if i != -1:
            spins[switch_number-1][y][x] = pg.transform.scale(snake_parts[i].picture, (64, 64))
            spin = 0
            snake_parts[i].picture = pg.image.load(images_path + '\\big_' + str(i) + '.png')


def creating_new_comand(I):
    global new_comand
    new_comand[I] = []
    for i in range(7):
        new_comand[I].append([-1, -1, -1, -1, -1, -1, -1])

def blitting_of_released():
    display.blit(pg.transform.scale(pg.image.load(images_path + "\\big_0.png"), (64, 64)), (cell_coords[0] + 3*64 + 3, cell_coords[1] + 3*64 + 3))
    
    for i in range(7):
        for j in range(7):
            if new_comand[switch_number-1][i][j] != -1 and not(i == j == 3) and new_comand[switch_number-1][i][j] != 0:
                display.blit(spins[switch_number-1][i][j], (cell_coords[0] + j*64 + j, cell_coords[1] + i*64 + i))


def saving():
    global snakes_data, new_comand
    for i in range(7):
        for j in range(7):

            if new_comand[switch_number-1][i][j] == 9:
                new_comand[switch_number-1][i][j] = 't1'
            elif 6 <= new_comand[switch_number-1][i][j] <= 8:
                new_comand[switch_number-1][i][j] = 'b1'
            elif i == j == 3:
                new_comand[switch_number-1][i][j] = 'h1'
                
            elif new_comand[switch_number-1][i][j] == 4:
                new_comand[switch_number-1][i][j] = 't2'
            elif 1 <= new_comand[switch_number-1][i][j] <= 3:
                new_comand[switch_number-1][i][j] = 'b2'
            elif new_comand[switch_number-1][i][j] == 0:
                new_comand[switch_number-1][i][j] = 'h2'
                
            elif new_comand[switch_number-1][i][j] == 10:
                new_comand[switch_number-1][i][j] = 'st'

            elif new_comand[switch_number-1][i][j] == -1:
                new_comand[switch_number-1][i][j] = 'nt'

    snakes_data[switch_number-1].append(new_comand[switch_number-1])
    creating_new_comand(switch_number-1)
    print(snakes_data[switch_number-1])


def analysis(I):
    global region, config
    x, y = int(moves[I][0][0]//30) - 3, int(moves[I][0][1]//30) - 3
    region[I] = []
    imposter = [-1, -1, -1, -1]

    for i in range(7):
        region[I].append(['fr', 'fr', 'fr', 'fr', 'fr', 'fr', 'fr'])

    for i in range(7):
        for j in range(7):
            if 0 <= y+i <= 19 and 0 <= x+j <= 19:
                x2, y2 = 30*(x+j), 30*(y+i)
                if config[y+i][x+j] == 2:
                    if not(i == 3 and j == 3):
                        region[I][i][j] = 'h2'
                    else:
                        region[I][i][j] = 'h1'

                elif config[y+i][x+j] == 1:
                    found = False
                    for k in range(4):
                        for l in range(1, 6):
                            if k != I and moves[k][l][0] == x2 and moves[k][l][1] == y2:
                                region[I][i][j] = 'b2'
                                found = True
                                break
                            elif not(found):
                                region[I][i][j] = 'b1'

                elif config[y+i][x+j] == 3:
                    found = False
                    for k in range(4):
                        if k != I and moves[k][6][0] == x2 and moves[k][6][1] == y2:
                            region[I][i][j] = 't2'
                            found = True
                            break
                        elif not(found):
                            region[I][i][j] = 't1'

            else:
                if ((y+i == -1 or y+i == 20) and (-1 <= x+j <= 20)) or ((x+j == -1 or x+j == 20) and (-1 <= y+i <= 20)):
                    region[I][i][j] = 'st'
                else:
                    region[I][i][j] = 'ed'

def rotate_mas(mas):
    global rotated_mas
    rotated_mas = []

    for i in range(7):
        rotated_mas.append([])
        for j in range(7):
            rotated_mas[i].append(mas[i][j])

    for j in range(7):
        for i in range(6, -1, -1):
            rotated_mas[i][j] = mas[j][6-i]


def print_snake(I):
    global equil
    equil = False
    remember(I)
    if not(dont_move[I]):
        for comand in snakes_data[I]:
            comparing(comand, region[I], I)
            if equil:
                break
        if not(equil):
            move(moves[I][0][0], moves[I][0][1], random.choice(['up', 'down', 'left', 'right']), I)
        changing_coords(I)

    prints(I, 'head' + str(I+1) + '.png', 'body' + str(I+1) + '.png', 'body' + str(I+1) + '_right.png', 'body' + str(I+1) + '_left.png', 'tail' + str(I+1) + '.png')


def comparing(comand, region, I):
    global equil
    equil = True
    shadow = []
    for i in range(7):
        shadow.append([])
        for j in range(7):
            shadow[i].append(comand[i][j])
    for i in range(7):
        for j in range(7):
            if shadow[i][j] != region[i][j] and shadow[i][j] != 'nt':
                equil = False
                break
    if equil:
        move(moves[I][0][0], moves[I][0][1], 'up', i)
    else:
        for angle in range(3):
            equil = True
            rotate_mas(shadow)
            for i in range(7):
                for j in range(7):
                    shadow[i][j] = rotated_mas[i][j]
            for i in range(7):
                if not(equil):
                    break
                for j in range(7):
                    if shadow[i][j] != region[i][j] and shadow[i][j] != 'nt':
                        equil = False
                        break
            if equil:
                if angle == 0:
                    move(moves[I][0][0], moves[I][0][1], 'left', I)
                elif angle == 1:
                    move(moves[I][0][0], moves[I][0][1], 'down', I)
                elif angle == 2:
                    move(moves[I][0][0], moves[I][0][1], 'right', I)
                break

def print_comand_and_region(I):
    for i in range(len(snakes_data[I])):
        for j in range(7):
            print(snakes_data[I][i][j])
        print()
    print()
    for i in range(7):
        print(region[I][i])
    print('>>>')




while Run:
    clock.tick(spd)
    mouse_pos = pg.mouse.get_pos()
    if Fight:

        display.blit(surface, (0, 0))

        fight_buttons()
        restore()
        for i in range(2):
            analysis(i)

            print_snake(i)

    if Menu:
        spd = 60

        display.blit(menu, (0, 0))

        menu_buttons()

    if Settings:
        spd = 60
        
        display.blit(settings, (0, 0))
        display.blit(pg.image.load(images_path + "\\cell.png"), (cell_coords[0], cell_coords[1]))
        
        draw_settings_buttons()
            
        for event in pg.event.get():
            snake_parts_registration()
            settings_buttons()
            
        blitting_of_released()
        


    pg.display.update()
    Quit_the_game()
