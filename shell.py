"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module:shell.py
"""

import pygame
pygame.init()
import random
import math
pygame.mixer.init()



"""sprite of shell1"""
class shell1(pygame.sprite.Sprite):
    
    """init function"""
    def __init__(self, dir):

        pygame.sprite.Sprite.__init__(self)

        #load image
        self.image = pygame.image.load("picture/shell1.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (2000, 2000)

        #move speed of y axis
        self.dy = 7 
        
        #direction left
        if dir == 0:
            self.image = pygame.transform.rotate(self.image, -30)
            self.dx = -2 

        #direction right
        else:
            self.image = pygame.transform.rotate(self.image, 30)
            self.dx = 2 
     
    """update function"""
    def update(self):

        #if not out of the screen
        if not (self.rect.left > 730 or self.rect.right < -10 or self.rect.top > 560):
            self.rect.centerx += self.dx
            self.rect.centery += self.dy
        #if out of the screen
        else:
            self.rect.center = (2000, 2000)
    
    """release function: set the postino within the screen"""
    def release(self, x, y):
        self.rect.center = (x, y)

    """reset function"""
    def reset(self):
        self.rect.center = (2000 , 2000)

"""shell2 sprite"""
class shell2(pygame.sprite.Sprite):
    
    """init function"""
    def __init__(self, picture, speed):

        pygame.sprite.Sprite.__init__(self)

        #load the image
        self.imageMaster = pygame.image.load(picture)
        self.imageMaster = self.imageMaster.convert_alpha()
        self.image = self.imageMaster
        self.rect = self.image.get_rect()

        #the direction
        self.dir = 0

        #the accurate speed
        self.realx = float() 
        self.realy = float()

        #the speed of int type
        self.dx = float() 
        self.dy = float() 
        
        #tell if it have been released
        self.released = False

        #speed
        self.speed = speed

        #reset
        self.reset()

    """reset function"""
    def reset(self):
        self.rect.center = (1500, 1500)
        self.released = False

    """update function"""
    def update(self):

        #if released is true
        if self.released:
            #if the the shell's position is within the screen
            if not (self.rect.right < 0 or self.rect.left > 720 or self.rect.bottom < -0 or self.rect.top > 540):
                #move
                self.realx += self.dx
                self.realy -= self.dy
                self.rect.centerx = self.realx
                self.rect.centery = self.realy
        #if not released, reset
        else:
            self.reset()

    
    """rotate function: rotate the image"""
    def rotate(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    """release function: release the shell at the position
        (x, y) with the direction dir"""
    def release(self, dir, x , y):
        self.rect.center = (x, y)
        self.realx = x
        self.realy = y
        self.released = True
        self.dir = dir
        self.rotate()
        self.calspeed()

    """calspeed function: calculate the speed of shell"""
    def calspeed(self):
        if self.dir != 0:
            dx = float(pygame.mouse.get_pos()[0] - self.rect.centerx)
            dy = float(pygame.mouse.get_pos()[1] - self.rect.centery)  
            bias = math.sqrt(dx * dx + dy * dy)
            dy *= -1
            self.dx = self.speed * dx / bias 
            self.dy = self.speed * dy / bias
        else:
            self.dx = 0
            self.dy = self.speed * -1
