import pygame, sys
from pygame.locals import *
import tkinter as tk
from functools import partial
import socket
from tkinter import messagebox
import time, random
import os


pygame.init()
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import screen

print(resource_path('bg.png'))

FPS = 60
fpsClock = pygame.time.Clock()

WINDOWWIDTH = 1000
WINDOWHEIGHT = 600

silver = (192, 192, 192)
light_silver = (211, 211, 211)

green = (0, 200, 0)
light_green = (0,255, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

BG = pygame.image.load(resource_path('bg.png'))
BG2 = pygame.image.load(resource_path('castle.png'))
dan = pygame.image.load(resource_path('Story1.png'))
dan = pygame.transform.scale(dan, (1000,600))

BG = pygame.transform.scale(BG, (1000, 600))
BG2 = pygame.transform.scale(BG2, (1200, 600))
tutorial_button = pygame.image.load(resource_path('2.png'))
tutorial_button1 = pygame.image.load(resource_path('2-1.png'))

menu = pygame.image.load(resource_path('1.png'))
menu1 = pygame.image.load(resource_path('1-NewGame.png'))
menu2 = pygame.image.load(resource_path('1-Tutorial.png'))
menu3 = pygame.image.load(resource_path('1-Quit.png'))

move1 = pygame.image.load(resource_path('dicpic1.png'))
move1 = pygame.transform.scale(move1, (300, 300))
move2 = pygame.image.load(resource_path('dicpic2.png'))
move2 = pygame.transform.flip(pygame.transform.scale(move2, (300, 300)), True, False)

huong_dan = pygame.image.load(resource_path('4.png'))
huong_dan1 = pygame.image.load(resource_path('4.1.png'))
huong_dan2 = pygame.image.load(resource_path('4.2.png'))

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('CARO')
clock = pygame.time.Clock()
pause = False

class Background():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = BG
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
    def draw(self):
        SCREEN.blit(self.img, (int(self.x), int(self.y)))

    def update(self, player1):
        x_camera = player1.x - (WINDOWWIDTH/2 - player1.width/2)
        if x_camera < 0:
            x_camera = 0
        if x_camera + WINDOWWIDTH > self.width:
            x_camera = self.width - WINDOWWIDTH
        self.x = -x_camera   


class Player1(): #Nhân vật chính
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = 0
        self.y = 270
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 0, 0))
        self.speed = 5
        self.test = False;
        self.m1 = move1 

    def draw(self, bg):
        SCREEN.blit(self.m1, (int(self.x), int(self.y)))
        

    def update(self, bg, left, right):
        if left == True:
            self.x -= self.speed
        if right == True:
            self.x += self.speed
        if self.x < 0:
            self.x = 0
        if self.x + self.width > bg.width:
            self.x = bg.width - self.width
          
        if abs(800 - self.x) <= 300:
            button('Click', 750, 350, 100, 50, light_silver, silver, talk1)

class Player2(): #Công chúa
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = 750
        self.y = 270
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))
        self.speed = 5

    def draw(self, bg):
        SCREEN.blit(move2, (int(self.x), int(self.y)))   

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(SCREEN, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("arial", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    SCREEN.blit(textSurf, textRect) 

def UnPause():
    global pause
    pause = False

def QuitGame():
    pygame.quit()
    quit()
   
def Paused():
    Text = pygame.font.SysFont("arial", 110)
    TextSurf, TextRect = text_objects("Paused", Text)
    TextRect.center = ((WINDOWWIDTH/2), (WINDOWHEIGHT/2) - 100)
    SCREEN.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        button("Continue", 350, 300, 100, 50, light_green, green, UnPause)
        button("Quit", 550, 300, 100, 50, light_red, red, game_intro)

        pygame.display.update()
        clock.tick(15)
  
def game_intro():
    action = Guide
    intro = True
    check = 1
    global pause
    pause = False
    temp = False
    SCREEN.blit(menu,(0,0))
    while intro:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            chuot = pygame.mouse.get_pos()
            if (chuot[0] >= 350 and chuot[0] <= 640) and (chuot[1] >= 215 and chuot[1] <= 300):
                SCREEN.blit(menu1,(0,0))
            elif (chuot[0] >= 350 and chuot[0] <= 640) and (chuot[1] >= 324 and chuot[1] <= 416) and (temp == False):
                SCREEN.blit(menu2,(0,0))
            elif (chuot[0] >= 350 and chuot[0] <= 640) and (chuot[1] >= 443 and chuot[1] <= 533) and (temp == False):
                SCREEN.blit(menu3,(0,0))
            elif temp == False: SCREEN.blit(menu,(0,0))

            
            if event.type == MOUSEBUTTONDOWN and check == 1:
                if (chuot[0] >= 370 and chuot[0] <= 640) and (chuot[1] >= 215 and chuot[1] <= 300):
                    action()
                    check = 0
                elif (chuot[0] >= 370 and chuot[0] <= 640) and (chuot[1] >= 324 and chuot[1] <= 416):
                    temp = True
                    SCREEN.blit(tutorial_button,(0,0))
                    check = 0
                elif (chuot[0] >= 370 and chuot[0] <= 640) and (chuot[1] >= 443 and chuot[1] <= 533):
                    temp = True
                    quit()
            
            elif event.type == MOUSEBUTTONDOWN and check == 0:
                if chuot[0] >= 16 and chuot[0] <= 156 and chuot[1] >= 15 and chuot[1] <= 82:
                    temp = False
                    SCREEN.blit(menu,(0,0))
                    check = 1
        pygame.display.update()
        clock.tick(15) 

def Guide():
    guided = True
    check = 1
    while guided:
        chuot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if chuot[0] >= 16 and chuot[0] <= 156 and chuot[1] >= 15 and chuot[1] <= 82:
                SCREEN.blit(huong_dan1,(0,0))
            elif chuot[0] >= 823 and chuot[0] <= 962 and chuot[1] >= 510 and chuot[1] <= 577:
                SCREEN.blit(huong_dan2,(0,0))
            else: SCREEN.blit(huong_dan,(0,0))
                    
            if event.type == MOUSEBUTTONDOWN:
                if chuot[0] >= 16 and chuot[0] <= 156 and chuot[1] >= 15 and chuot[1] <= 82:
                    game_intro()
                elif chuot[0] >= 823 and chuot[0] <= 962 and chuot[1] >= 510 and chuot[1] <= 577:
                    game_loop()
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global pause
    bg = Background()
    player1 = Player1()
    player2 = Player2()
    left = False
    right = False
    check = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_p:
                    pause = True
                    Paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
           
        bg.draw()
        player1.draw(bg)

        player1.update(bg, left, right)
        bg.update(player1)
        
        player2.draw(bg)
        pygame.display.update()
        fpsClock.tick(FPS)

def talk1():
    SCREEN.blit(dan,(0,0))
    step = 0
    smallText = pygame.font.SysFont("Roboto", 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    Paused()
            if event.type == MOUSEBUTTONDOWN:
                step += 1
                if step == 1:
                    temp = pygame.image.load(resource_path('Prince-1.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 2:
                    temp = pygame.image.load(resource_path('Princess-1.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 3:
                    temp = pygame.image.load(resource_path('Princess-2.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 4:
                    temp = pygame.image.load(resource_path('2Prince-1.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 5:
                    temp = pygame.image.load(resource_path('2Prince-2.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 5:
                    temp = pygame.image.load(resource_path('2King-1.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 6:
                    temp = pygame.image.load(resource_path('2King-2.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 7:
                    temp = pygame.image.load(resource_path('2Prince-3.png'))
                    temp = pygame.transform.scale(temp, (1000,600))
                    SCREEN.blit(temp,(0,0))
                if step == 8:
                    afterez()
        pygame.display.update()

def afterez():
    step = 0
    smallText = pygame.font.SysFont("Roboto", 30)
    result = screen.rungame(1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    Paused()
            if event.type == MOUSEBUTTONDOWN:
                step += 1
                if result == 'O' or result == ' ':
                    if step == 1:
                        temp = pygame.image.load(resource_path('B1.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 2:
                        temp = pygame.image.load(resource_path('K1.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 3:
                        temp = pygame.image.load(resource_path('P1.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 4:
                        temp = pygame.image.load(resource_path('K2.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 5:
                        temp = pygame.image.load(resource_path('P2.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 6: 
                        afternor() #test lát xóa
                else:
                    if step == 1:
                        temp = pygame.image.load(resource_path('P4.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 2:
                        temp = pygame.image.load(resource_path('P4.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 3: quit()
        pygame.display.update()

def afternor():
    #X: nguoi choi thang, O: AI thang, ' ': hoa
    step = 0
    smallText = pygame.font.SysFont("Roboto", 30)
    result = screen.rungame(3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    Paused()
            if event.type == MOUSEBUTTONDOWN:
                step += 1
                if result == 'O' or result == ' ':
                    if step == 1:
                        temp = pygame.image.load(resource_path('K3.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 2:
                        temp = pygame.image.load(resource_path('K4.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 3:
                        temp = pygame.image.load(resource_path('P3.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 4: 
                        afterhard()
                else:
                    if step == 1:
                        temp = pygame.image.load(resource_path('K5.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
        pygame.display.update()

def afterhard():
    #X: nguoi choi thang, O: AI thang, ' ': hoa
    step = 0
    smallText = pygame.font.SysFont("Roboto", 30)
    result = screen.rungame(5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    Paused()
            if event.type == MOUSEBUTTONDOWN:
                step += 1
                if result == 'O' or result == ' ':
                    if step == 1:
                        temp = pygame.image.load(resource_path('K6.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 2:
                        temp = pygame.image.load(resource_path('P5.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 3:
                        temp = pygame.image.load(resource_path('P6.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 4:
                        temp = pygame.image.load(resource_path('K7.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 5:
                        temp = pygame.image.load(resource_path('K8.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 6:
                        temp = pygame.image.load(resource_path('P7.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 7:
                        temp = pygame.image.load(resource_path('pr1.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 8:
                        temp = pygame.image.load(resource_path('P8.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                    if step == 9:
                        temp = pygame.image.load(resource_path('pr2.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
                else:
                    if step == 1:
                        temp = pygame.image.load(resource_path('K10.png'))
                        temp = pygame.transform.scale(temp, (1000,600))
                        SCREEN.blit(temp,(0,0))
        pygame.display.update()

game_intro()
pygame.quit()
quit()