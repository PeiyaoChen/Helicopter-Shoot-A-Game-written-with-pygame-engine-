"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Artillery
"""
import pygame
import random
import math
import shell
pygame.init()
pygame.mixer.init()

"""Artillery sprite"""
class Artillery(pygame.sprite.Sprite):
    
    """init function"""
    """picturename is the artillery's picture name, shellnmae is the shell picture's
        name, IsFollowMouse tell whether the artillery rotate following mouse,
        frequency is the frequency of releasing shells(lower more frequently),
        speed is the moving speed of the shell"""

    def __init__(self, picturename, shellname, IsFollowMouse, frequency, speed):

        pygame.sprite.Sprite.__init__(self)

        #load image
        self.imageMaster = pygame.image.load(picturename)
        self.imageMaster = self.imageMaster.convert_alpha()
        self.image = self.imageMaster
        self.rect = self.image.get_rect()

        #shell list
        self.shells = []

        #delay
        self.rdelay = 2
        self.rpause = 0

        #artillery picture name
        self.picture = picturename

        #tell if have released the shells
        self.haveReleased = False

        #release times
        self.retimes = 0
        
        #tell which shell to be released
        self.shellindex = 0

        #if rotate following mouse
        self.IsFollowMouse = IsFollowMouse

        #relase shell frequency
        self.frequency = frequency
        for i in range(0, 30):
            theshell = shell.shell2(shellname, speed)
            self.shells.append(theshell)
        self.reset()

    """reset function"""
    def reset(self):
        self.image = pygame.image.load(self.picture)
        self.image = self.image.convert_alpha()
        self.haveReleased = False

    """update function"""
    def update(self):
        self.followMouse()
        self.rotate()
        if self.haveReleased:
            self.release()
        else:
            if random.randrange(0, self.frequency) == 0:
                self.haveReleased = True

    """followMouse function: change the rotate angle"""
    def followMouse(self):
        if self.IsFollowMouse:
            dx = pygame.mouse.get_pos()[0] - self.rect.centerx
            dy = pygame.mouse.get_pos()[1] - self.rect.centery

            dy *= -1
            radians = math.atan2(dy, dx)
            self.dir = radians * 180/math.pi + 90
            
        else:
            self.dir = 0 

    """rotate function: rotate the image of artillery"""
    def rotate(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        radians = (self.dir - 90) * math.pi / 180
        dx = math.cos(radians) * 10
        dy = math.sin(radians) * (-10)
        self.rect.center = (oldcenter[0] + dx, oldcenter[1] + dy)

    """release function: release the shells"""
    def release(self):
        self.rpause += 1
        if self.rpause == self.rdelay:

            radians = (self.dir - 90) * math.pi / 180

            x = self.rect.centerx + math.cos(radians) * 30
            y = self.rect.centery - math.sin(radians) * 30

            self.shells[self.shellindex].release(self.dir, x, y)
            
            self.retimes += 1
            self.shellindex += 1

            if self.shellindex == 29:
                self.shellindex =0
            if self.retimes == 1:
                self.retimes = 0
                self.haveReleased = False
            self.rpause = 0
