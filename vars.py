import pygame as pg
import random
import os, sys
import comands
from comands import *
# переменные
X, Y = int(1.5*770), int(1.5*570)
k = X / 800
size = Y // 19
amount = 4
current_path = os.path.dirname(__file__)
resources_path = os.path.join(current_path, 'resources')
font_path = os.path.join(resources_path, 'fonts')
images_path = os.path.join(resources_path, 'images')

clock = pg.time.Clock()
display = pg.display.set_mode((X, Y))
keys = pg.key.get_pressed()


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
grabbed = [False] * 12
region = [[], [], [], []]
spin = 0
spd = 5
snake_parts = [0]*12
cell_coords = (73, 145)
face_spin = 0

snakes_data = [[], [], [], []]



snakes_data[0].extend(tail)
##snakes_data[1].extend(tail)
##snakes_data[2].extend(tail)
##snakes_data[3].extend(tail)
##
##snakes_data[0].extend(basic)
##snakes_data[1].extend(basic)
##snakes_data[2].extend(basic)
##snakes_data[3].extend(basic)

##snakes_data[0].extend(circle)
##snakes_data[2].extend(left1)
##snakes_data[3].extend(left2)


