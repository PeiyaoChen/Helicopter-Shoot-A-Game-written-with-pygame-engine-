"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Boss.py
"""
import pygame
import random
import math
import shell
import Helicopter
import Explode
import Artillery
pygame.init()
pygame.mixer.init()

"""function to change the color of image to yellow"""
def changeColor(surface):
    for col in range(0, surface.get_width()):
        for row in range(0, surface.get_height()):
            (r, g, b, a) = surface.get_at((col, row))
            if a != 0:
                r = r + 200
                if r > 255:
                    r = 255
                g = g+ 100
                if g > 255:
                    g = 255
                surface.set_at((col, row), (r, g, b , a))
    return surface

"""PowerRect sprite, show the rectangle represents the power of boss"""
class PowerRect(pygame.sprite.Sprite):
    
    """init function"""
    def __init__(self, color, unitwidth):
        pygame.sprite.Sprite.__init__(self)

        #color
        self.color = color
        #power value
        self.power = 30 

        #surface
        self.image = pygame.Surface((90, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.left = 100 
        self.rect.bottom = 530 

        #width of one power
        self.unitwidth = unitwidth

    """update function"""
    def update(self):
        if self.power >= 0:
            self.image = pygame.Surface((self.power * self.unitwidth, 10))
            self.image.fill(self.color)

    def setPower(self, power):
        self.power = power


class Boss(pygame.sprite.Sprite):

    """init function"""
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        #body image
        self.image = pygame.image.load("picture/bossbody.png")
        self.image = self.image.convert_alpha()
        self.imageMaster = self.image
        
        #image while being attacked
        self.imageAttacked = pygame.image.load("picture/bossbody.png")
        self.imageAttacked = self.imageAttacked.convert_alpha()
        self.imageAttacked = changeColor(self.imageAttacked)
        
        self.beAttacked = False
        self.attackedIndex = 0

        self.rect = self.image.get_rect()

        #moving speed
        self.dx = 2 
        self.dy = 0

        #live 
        self.live = 300 

        #moving direction
        self.dir = 0

        #4 artilleries
        self.artillery = Artillery.Artillery("picture/bossartillery.png", "picture/shell4.png", 1, 70, 20)
        self.artillery1 = Artillery.Artillery("picture/bossartillery3.png", "picture/shell2.png", 0, 40, 15)
        self.artillery4 = Artillery.Artillery("picture/bossartillery3.png", "picture/shell2.png", 0, 40, 15)
        self.artillery3 = Artillery.Artillery("picture/bossartillery4.png", "picture/shell3.png", 1, 10, 10)
        self.artillery2 = Artillery.Artillery("picture/bossartillery4.png", "picture/shell3.png", 1, 10, 10)
        
        #artillery list
        self.artilleryList = [self.artillery, self.artillery1, self.artillery2, self.artillery3, self.artillery4]

        #reset
        self.reset()

        #tell if is being destroyed
        self.destroyed = False

        #3 explodes
        self.explode = Explode.Explode(120)
        self.explode2 = Explode.Explode(150)
        self.explode3 = Explode.Explode(100)

        #explode list
        self.explodeList = [self.explode, self.explode2, self.explode3]

        #explode count
        self.explodeCount = 0

        #tell if it begins to explode
        self.beginExplode = False
        

        
        #angle of the image rotate
        angle = 90

        #rotaete
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.imageMaster = pygame.transform.rotate(self.imageMaster, angle)
        self.imageAttacked = pygame.transform.rotate(self.imageAttacked, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        
        #power rectangle
        self.powerRect = PowerRect((0, 0, 255), 2)
        self.powerRect.power = self.live
        self.powerRect.rect.left = 30
        self.powerRect.rect.top = 10

    """reset function"""
    def reset(self):
        self.rect.centerx = -100
        self.rect.centery =  100
        for i in range(0, 5):
            self.artilleryList[i].reset()
        self.beAttacked = False
        self.explodeCount = 0
        self.beginExplode = False

        
    """update function"""
    def update(self):

        #powerRect's power is equal to live
        self.powerRect.power = self.live

        #if it is being attacked
        if self.beAttacked:
            #blink
            self.attackedIndex += 1
            if (self.attackedIndex / 2) % 2 == 0:
                self.image = self.imageAttacked
            else:
                self.image = self.imageMaster
            if self.attackedIndex >= 20:
                self.beAttacked = False
                self.attackedIndex = 0
                self.image = self.imageMaster

        #if dir is 0, move right
        if self.dir == 0:
            self.rect.centerx += self.dx
        #if dir is 1, move left
        else:
            self.rect.centerx -= self.dx

        #if arriving the end, move backward
        if self.dir == 0 and self.rect.right >= 720:
            self.dir = 1
        if self.dir == 1 and self.rect.left <= 0:
            self.dir = 0

        self.rect.centery += self.dy
        
        
        if self.rect.centery > 600:
            self.reset()
            self.artillery.reset()
            for i in range(0, 5):
                self.artilleryList[i].reset()
        
        #set the position of artilleries
        self.artillery.rect.center = (self.rect.centerx, self.rect.centery)
        self.artillery1.rect.center = (self.rect.centerx - 26, self.rect.centery - 27)
        self.artillery2.rect.center = (self.rect.centerx + 26, self.rect.centery - 43)
        self.artillery3.rect.center = (self.rect.centerx - 26, self.rect.centery + 25)
        self.artillery4.rect.center = (self.rect.centerx + 26, self.rect.centery + 42)

        #if beginExplode is true
        if self.beginExplode:
            
            #call the 3 eploxdes in order
            self.explodeCount += 1
            if self.explodeCount == 1:
                self.explode.start_explode(self.rect.centerx, self.rect.centery)
            if self.explodeCount == 5:
                self.explode2.start_explode(self.rect.centerx + 50, self.rect.centery)
            if self.explodeCount == 10:
                self.explode3.start_explode(self.rect.centerx - 50, self.rect.centery)
            if self.explodeCount >= 15:
                self.reset()

    """function toExplode: called when it is to explode"""
    def toExplode(self):
        self.beginExplode = True
        self.dx = 0
        
    """function attacked: called when attacked"""
    def attacked(self):
        self.live -= 1
        self.beAttacked = True
