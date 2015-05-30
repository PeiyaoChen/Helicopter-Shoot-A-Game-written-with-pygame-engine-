"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module:Helicopter.py
"""

"""Helicopter Module"""

import pygame
import random
import math
import shell
import Shadow
import Explode
import Laser
pygame.init()
pygame.mixer.init()


        
"""the function that change the color of image to yellow.
    While attacked it will be called"""
def changeColor(surface):
    #get the color of every pixel, and change the green and red bits
    for col in range(0, surface.get_width()):
        for row in range(0, surface.get_height()):
            (r, g, b, a) = surface.get_at((col, row))   #get the ARGB of the pixel
            #change the green and red bits of the nontransparent pixel
            if a != 0:
                r = r + 200
                if r > 255:
                    r = 255
                g = g+ 100
                if g > 255:
                    g = 255
                surface.set_at((col, row), (r, g, b , a))
    return surface


"""The sprite of helicopter"""
class Helicopter(pygame.sprite.Sprite):
    def __init__(self, propeller):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/helicopter.png") 
        self.iamge = self.image.convert_alpha()
        self.imageMaster = self.image   #the normal image

        #the image when attacked
        self.imageAttacked = pygame.image.load("picture/helicopter.png") 
        self.imageAttacked = self.imageAttacked.convert_alpha()
        self.imageAttacked = changeColor(self.imageAttacked)

        self.rect = self.image.get_rect()
        
        #the propeller of the helicopter
        self.propeller = propeller
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)

        #the larsers, total number is 30
        self.lasers = []
        for i in range(0, 30):
            thelaser = Laser.Laser()
            self.lasers.append(thelaser)

        #laser index, determine which laser is released
        self.laserIndex = 0
        
        #delay of releasing laser
        self.releaseDelay = 2
        self.releasePause = 0

        #live of helicopter
        self.live = 30 

        #flag determine if the helicopter is being attacked
        self.beAttacked = False

        #being attacked once, the helicopter will blink,
        #this variable is to count the blink times
        self.attackedIndex = 0

        #the shadow of the helicopter
        self.shadow = Shadow.Shadow("picture/helishadow.png")

        #flag tell whether the helicopter begins exploding
        self.beginExplode = False

        #Explode sprite
        self.explode = Explode.Explode(100)

        
    """the update function"""        
    def update(self):
        #if helicopter have not begun exploded 
        if not self.beginExplode:
            #if helicopter is being attacked,change between the
            #yellow image and the normal image
            if self.beAttacked:
                self.attackedIndex += 1
                if (self.attackedIndex / 3) % 2 == 0:
                    self.image = self.imageAttacked
                else:
                    self.image = self.imageMaster
                if self.attackedIndex == 9:
                    self.attackedIndex = 0
                    self.beAttacked = False
                    self.image = self.imageMaster
                    
            #update the shadow and the propeller
            self.rect.center = pygame.mouse.get_pos()
            self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
            self.shadow.rect.center = (self.rect.centerx - 20, self. rect.centery - 15)
            #helicopter release laser if clicking the mouse
            self.check_mouse()
        #if helicopter has begun exploding
        else:
            self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
            self.shadow.rect.center = (self.rect.centerx - 20, self. rect.centery - 15)

    """function to check mouse's left click"""
    def check_mouse(self):
        if pygame.mouse.get_pressed()[0]:

            self.releasePause += 1

            if self.releasePause >= self.releaseDelay:
                self.lasers[self.laserIndex].release(self.rect.centerx, self.rect.centery - 30)
                self.laserIndex += 1

                if(self.laserIndex >= 30):
                    self.laserIndex = 0

                self.releasePause = 0

    """The function is called when attacked"""
    def attacked(self):
        self.beAttacked = True
    
    """The function is called when to explode"""
    def toExplode(self):
        self.beginExplode = True
        self.explode.start_explode(self.rect.centerx, self.rect.centery)
        self.rect.center = (1000, 1000)
