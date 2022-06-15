from ast import walk
from operator import le
from tkinter.tix import Tree
from tracemalloc import start
from turtle import right, title, width
import random
import pygame
import sys
from pygame.constants import KEYDOWN, K_ESCAPE, K_KP1, MOUSEBUTTONDOWN, NUMEVENTS, QUIT, K_e
pygame.init()


win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ninjas In Paris")

walkLeft = [
    pygame.image.load("bin/Police L1.png"),
    pygame.image.load("bin/Police L2.png"),
    pygame.image.load("bin/Police L3.png"),
    pygame.image.load("bin/Police L4.png"),
    pygame.image.load("bin/Police L5.png"),
    pygame.image.load("bin/Police L6.png"),
    pygame.image.load("bin/Police L7.png"),
    pygame.image.load("bin/Police L8.png"),
    pygame.image.load("bin/Police L9.png")]
walkRight = [
    pygame.image.load("bin/Police R1.png"),
    pygame.image.load("bin/Police R2.png"),
    pygame.image.load("bin/Police R3.png"),
    pygame.image.load("bin/Police R4.png"),
    pygame.image.load("bin/Police R5.png"),
    pygame.image.load("bin/Police R6.png"),
    pygame.image.load("bin/Police R7.png"),
    pygame.image.load("bin/Police R8.png"),
    pygame.image.load("bin/Police R9.png")]
char = pygame.image.load("bin/Police.png")
bg = pygame.image.load("bin/back.jpg")
proj = pygame.image.load("bin/bullet.png")
pl = pygame.image.load("bin/platform.png")
title = pygame.image.load("bin/title.png")


bulletSound = pygame.mixer.Sound('bin/Tap.mp3')
reloadSound = pygame.mixer.Sound('bin/Reload.mp3')
hitSound = pygame.mixer.Sound('bin/Hit.mp3')
music = pygame.mixer.Sound('bin/Music.mp3')
music.play(-1)

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.vel= 3
        self.isJump= False
        self.jumpCount= 10
        self.left = False
        self.right = False
        self.walkCount= 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw(self, win):
        if self.walkCount + 1 >=27:
            self.walkCount = 0

        # if not (self.standing):
        if self.left:
            win.blit(walkLeft[self.walkCount//6], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//6], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))
        self.hitbox = (self.x + 20, self.y, 28, 60)
        # pygame.draw.rect(win, (0,255,0), self.hitbox, 2)

class enemy(object):
    walkLeft = pygame.image.load("bin/ninja L1.png")
    walkRight = pygame.image.load("bin/ninja R1.png")

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 100
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 40, 60)
        self.visible = True
        
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.vel >0:
                win.blit(self.walkRight, (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft, (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 20, self.y, 40, 60)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    def hit(self):
        if self.health > 0:
            self.health -= random.randint(1,10)
        else:
            self.visible = False
            hitSound.play()
        print ('hit')
        

class platform(object):
    def __init__(self,x,y,height,width):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
    
    def draw(self,win):
        win.blit(pl, (self.x, self.y))
        
 
class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 12 * facing

    def draw(self, win):
        win.blit(proj, (self.x,self.y))

def game():
    font_1 = pygame.font.Font("bin/LuckiestGuy.ttf", 16,)
    font_12 = pygame.font.Font("bin/LuckiestGuy.ttf", 28,)
    font_2 = pygame.font.Font("bin/LuckiestGuy.ttf", 32,)
    font_3 = pygame.font.Font("bin/LuckiestGuy.ttf", 64,)
    font_4 = pygame.font.Font("bin/LuckiestGuy.ttf", 128,)
    shootLoop = 0
    bullets = []
    police = player(100, 500-60, 64, 64)
    ninja = enemy(300,500-60, 64, 64, 750)
    plats = []
    plat = platform(0, 500, 64, 128)
    # platform(0, 500, 64, 128)
    num_of_bullets = 17
    run = True
    while run:
        global walkCount
        win.blit(bg, (0,0))
        ammo = font_3.render(str(num_of_bullets+1), 1, (241,241,241))
        magzine= font_2.render(" / " + str(18), 1, (241,241,241))
        reload = font_1.render("Press R to Reload", 1, (241,241,241))
        win.blit(ammo, (10, 20))
        win.blit(magzine, (70, 40))
        police.draw(win)
        ninja.draw(win)
        plat.draw(win)

        for bullet in bullets:
            bullet.draw(win)

        if num_of_bullets < 17:
            win.blit(reload, (10, 80))

        pygame.display.update()

        clock.tick(60)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    titleScreen()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        for bullet in bullets:
            if bullet. y < ninja.hitbox[1] + ninja.hitbox[3] and bullet.y > ninja.hitbox [1]:
                if bullet.x > ninja.hitbox[0] and bullet.x < ninja.hitbox[0] + ninja.hitbox[2]:
                    ninja.hit()
                    bullets.pop(bullets.index(bullet))
            if bullet.x < 780 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop==0 :
            if police.left:
                facing = -1
            else:
                facing = 1
            if num_of_bullets <= 17 > 0:
                if len(bullets) <= num_of_bullets:
                    bullets.append(projectile(round(police.x + police.width//4), round(police.y + police.height//7), facing))
                    num_of_bullets -= 1
                    bulletSound.play()
            elif num_of_bullets <= 0:
                num_of_bullets == 0
            shootLoop = 1


        if keys[pygame.K_r]:
            if num_of_bullets < 17:
                num_of_bullets = +17
                reloadSound.play()

        if keys[pygame.K_LEFT] and police.x > 0:
            police.x -= police.vel
            police.left = True
            police.right = False
            police.standing = False
        elif keys[pygame.K_RIGHT] and police.x < 800 - police.width:
            police.x += police.vel
            police.right = True
            police.left = False
            police.standing = False
        else:
            police.standing = True
            police.right = False
            police.left = False
            walkCount = 0

        if not(police.isJump):
            if keys [pygame.K_UP] and ninja.y < 600 - police.height:
                police.isJump = True
                police.right = False
                police.left = False
                police.walkCount = 0
        else:
            if police.jumpCount >= -10:
                neg = 1
                if police.jumpCount < 0:
                    neg = -1
                police.y -= (police.jumpCount ** 2)*0.5*neg
                police.jumpCount -= 1

            else:
                police.isJump = False
                police.jumpCount = 10

def titleScreen():
    font_1 = pygame.font.Font("bin/LuckiestGuy.ttf", 16,)
    font_12 = pygame.font.Font("bin/LuckiestGuy.ttf", 28,)
    font_2 = pygame.font.Font("bin/LuckiestGuy.ttf", 32,)
    font_3 = pygame.font.Font("bin/LuckiestGuy.ttf", 64,)
    font_4 = pygame.font.Font("bin/LuckiestGuy.ttf", 128,)
    shootLoop = 0
    bullets = []
    police = player(100, 500-60, 64, 64)
    ninja = enemy(300,500-60, 64, 64, 750)
    plats = []
    plat = platform(0, 500, 64, 128)
    # platform(0, 500, 64, 128)
    num_of_bullets = 17
    run = True
    while run:
        global walkCount
        win.blit(bg, (0,0))
        ammo = font_3.render(str(num_of_bullets+1), 1, (241,241,241))
        magzine= font_2.render(" / " + str(18), 1, (241,241,241))
        reload = font_1.render("Press R to Reload", 1, (241,241,241))
        shoot = font_1.render("Shoot = SPACEBAR", 1, (255,230,0))
        move = font_1.render("Move = Left and Right Arrow", 1, (255,230,0))
        jump = font_1.render("Jump = UP Arrow", 1, (255,230,0))
        sub = font_12.render("Kill The Ninja To Start", 1, (241,241,241))
        win.blit(ammo, (10, 20))
        win.blit(magzine, (70, 40))
        win.blit(move, (110, 560))
        win.blit(jump, (350, 560))
        win.blit(shoot, (500, 560))
        win.blit(sub, (400, 350))
        police.draw(win)
        ninja.draw(win)
        plat.draw(win)
        win.blit(title, (0,40))

        for bullet in bullets:
            bullet.draw(win)

        if num_of_bullets < 17:
            win.blit(reload, (10, 80))

        pygame.display.update()

        clock.tick(60)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        for bullet in bullets:
            if bullet. y < ninja.hitbox[1] + ninja.hitbox[3] and bullet.y > ninja.hitbox [1]:
                if bullet.x > ninja.hitbox[0] and bullet.x < ninja.hitbox[0] + ninja.hitbox[2]:
                    ninja.hit()
                    bullets.pop(bullets.index(bullet))
            if bullet.x < 780 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop==0 :
            if police.left:
                facing = -1
            else:
                facing = 1
            if num_of_bullets <= 17 > 0:
                if len(bullets) <= num_of_bullets:
                    bullets.append(projectile(round(police.x + police.width//4), round(police.y + police.height//7), facing))
                    num_of_bullets -= 1
                    bulletSound.play()
            elif num_of_bullets <= 0:
                num_of_bullets == 0
            shootLoop = 1


        if keys[pygame.K_r]:
            if num_of_bullets < 17:
                num_of_bullets = +17
                reloadSound.play()

        if keys[pygame.K_LEFT] and police.x > 0:
            police.x -= police.vel
            police.left = True
            police.right = False
            police.standing = False
        elif keys[pygame.K_RIGHT] and police.x < 880 - police.width:
            police.x += police.vel
            police.right = True
            police.left = False
            police.standing = False
        else:
            police.standing = True
            police.right = False
            police.left = False
            walkCount = 0

        if not(police.isJump):
            if keys [pygame.K_UP] and ninja.y < 600 - police.height:
                police.isJump = True
                police.right = False
                police.left = False
                police.walkCount = 0
        else:
            if police.jumpCount >= -10:
                neg = 1
                if police.jumpCount < 0:
                    neg = -1
                police.y -= (police.jumpCount ** 2)*0.5*neg
                police.jumpCount -= 1

            else:
                police.isJump = False
                police.jumpCount = 10
        if police.x > 800:
            game()
        pygame.display.update()
titleScreen()