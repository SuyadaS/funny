import pygame
from pynput import mouse
from network import Network
pygame.font.init()
import os
import threading
import time

width = 500
height = 500
n = Network()
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")
click_count = 0
flag = 0

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BG.jpg")), (width, height))
BG_wait = pygame.transform.scale(pygame.image.load(os.path.join("assets", "gameBG.jpg")), (width, height))

# Player player
bird1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "b1.png")), (100,80))
bird2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "b3.png")), (100,80))

#win lose BG
u_win =  pygame.transform.scale(pygame.image.load(os.path.join("assets", "win.jpg")), (width, height))
u_lose = pygame.transform.scale(pygame.image.load(os.path.join("assets", "lose.jpg")), (width, height))

class Player():
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bird = (x,y,width,height)
        self.vel = 3
        self.ready = False 
        self.image = image
           
    def draw(self,win):
        win.blit(self.image, (self.x, self.y))
        
    def move(self):
        self.x += self.vel
        self.update()
                
    def update(self):
        self.bird = (self.x, self.y, self.width, self.height)
        
    def get_width(self):
        return self.image.get_width()
        
def read_pos(str):
    str = str.split(",")
    return int(str[0]) , int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def read_check(str):
    if str == "True":
        return True
    else:
        return False
               
def redrawWindow(win,p,p2):
    win.blit(BG_wait, (0,0))

    if not(p.ready and p2.ready):
        wait = pygame.transform.scale(pygame.image.load(os.path.join("assets", "waiting.png")), (300,250))
        win.blit(wait, (width/2 - wait.get_width()/2, height/2 - wait.get_height()/2))
    else:
        p.draw(win)
        p2.draw(win)
    pygame.display.update()

def countclick(p):
    global flag
    global click_count
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        if flag ==1:
            print("ending the thread")
            break
        else:
            click_count = p.x/3
            print (click_count)
            
        
def main(boo1,boo2):
    global click_count
    global flag
    t = time.time()
    run = boo1
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],100,100,bird1)
    p2 = Player(0,0,100,100,bird2)
    p.ready = boo2
    clock = pygame.time.Clock()

    tcount = threading.Thread(target=countclick, args=(p,))
    tcount.setDaemon(True)
    tcount.start()

    while run:
        clock.tick(60)
        p2.ready = read_check(n.send(str(p.ready)))
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        if p.x + p.get_width() > width:
            flag = 1
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("You've clicked"+ str(click_count) + "times in" + str(time.time() - t), 1, (255,0,0)) 
            win.blit(u_win, (0,0))
            pygame.display.update()
            pygame.time.delay(2000)
            win.blit(text, (width/100 - text.get_width()/100, height/100 - text.get_height()/100))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False            
        elif p2.x + p2.get_width() > width:
            flag = 1
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("You've clicked"+ str(click_count) + "times in" + str(time.time() - t), 1, (255,0,0)) 
            win.blit(u_lose, (0,0))
            pygame.display.update()
            pygame.time.delay(2000)
            win.blit(text, (width/100 - text.get_width()/100, height/100 - text.get_height()/100))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]: 
                    p.move()
        redrawWindow(win ,p , p2)
    tcount.join()
    print("thread end")
    click_count = 0
    flag = 0
    n.reset(1)
    menu(True)
        
def menu(boo):
    run = boo
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.blit(BG, (0,0))
        start = pygame.image.load(os.path.join("assets", "start.png"))
        win.blit(start, (10,70))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False                  
    main(True,True)       

while True:
    menu(True)