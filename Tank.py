"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Tank.py
"""

"""the tank module"""

import pygame
import random
import math
import shell
import Helicopter
import Shadow
import Explode
import Fighter 
import Artillery
pygame.init()
pygame.mixer.init()



"""tank sprite"""
class Tank(pygame.sprite.Sprite):
    
    """init fuction"""
    def __init__(self, direction, stopx, resetx):
        pygame.sprite.Sprite.__init__(self)
        
        #if stop is true, it well not move
        self.stop = False
        
        #count the frame
        self.timeCount = 0
        
        #load the image of the tank body
        self.image = pygame.image.load("picture/tankbody.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        #move direction, 0 is to right, 1 is to left
        self.dir = direction

        #speed
        self.dx = 0
        self.dy = 2

        #live
        self.live = 2

        #stop postion of x
        self.stopx = stopx

        
        self.resetx = resetx

        #initialize the artillery
        self.artillery = Artillery.Artillery("picture/artillery.png", "picture/shell2.png", 1, 50, 10)
        self.reset()
        self.destroyed = False

        #initialize the explode
        self.explode = Explode.Explode(100)

        if self.dir == 0:
            angle = 90
        else:
            angle = -90

        #original center
        oldcenter = self.rect.center
    
        #rotate the image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    """reset function"""
    def reset(self):
        if self.dir == 0:
            self.rect.centerx = -self.resetx
            self.dx = 2
        else:
            self.rect.centerx = 720 + self.resetx
            self.dx = -2
        self.rect.centery = random.randrange(0, 100)
        self.artillery.reset()
        self.live = 2
        if self.timeCount >= 900:
            self.stop = True
        
    """update function"""
    def update(self):
        
        self.timeCount += 1

        #if stop is false
        if not self.stop: 
            #if timeCount is 900
            if self.timeCount == 900:
                self.dy -= 2
            
            #if dir is 0, move to right
            if self.dir == 0 and self.rect.centerx <= self.stopx:
                self.rect.centerx += self.dx

            #if dir is 1, move to left
            if self.dir == 1 and self.rect.centerx >= self.stopx:
                self.rect.centerx += self.dx

            self.rect.centery += self.dy

            #if it is out of the screen, reset
            if self.rect.top > 600:
                self.reset()
                self.artillery.reset()

        #different direction the artillery postion
        #on the tank body image is different
        if self.dir == 0:
            self.artillery.rect.center = (self.rect.centerx + 10, self.rect.centery)
        else:
            self.artillery.rect.center = (self.rect.centerx - 10, self.rect.centery)

    
    """Funtion toExplode:if the tank explode, it will be called"""
    def toExplode(self):
        self.explode.start_explode(self.rect.centerx, self.rect.centery)
        self.reset()

    """Function attacked: if attacked, it will be called""" 
    def attacked(self):
        self.live -= 1
        
