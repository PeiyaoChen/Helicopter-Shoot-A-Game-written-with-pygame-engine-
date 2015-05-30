"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Soldier.py
"""
import pygame
import random
import math
import shell
pygame.init()
pygame.mixer.init()


"""Soldier sprite"""
class Soldier(pygame.sprite.Sprite):

    """init function"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #time count
        self.timeCount = 0
        self.stop = False

        #soldier walking image
        self.image = pygame.image.load("picture/walking0.png")
        self.rect = self.image.get_rect()

        #shell list
        self.shells = []

        #shell releasing delay
        self.rdelay = 2
        self.rpause = 0

        #tell wether the shell have been released
        self.haveReleased = False

        #release times
        self.retimes = 0

        #shell index, tell which shell to be released
        self.shellindex = 0

        #wlking images list
        self.walkimages = [] 
        #dying image list
        self.dieimages = []
        
        #walking image index
        self.walkindex = 0
        #dying iamge index
        self.dieindex = 0

        #speed of y axis
        self.dy = 3

        #tell whether dying
        self.dying = False
        
        #live
        self.live = 2

        #cry sound, played when died
        self.sound = pygame.mixer.Sound("sound/cry.ogg")
        
        #load the walking images
        i = 0
        while i < 16:
            theimage = pygame.image.load("picture/walking%d.png" %i)
            theimage = theimage.convert_alpha()
            self.walkimages.append(theimage)
            i += 1

        #load the dying image
        i = 0
        while i < 10:
            theimage = pygame.image.load("picture/die%d.png" %i)
            theimage = theimage.convert_alpha()
            self.dieimages.append(theimage)
            i += 1
        #load the died image
        theimage = pygame.image.load("picture/die9.png")
        theimage = theimage.convert_alpha()
        for t in range(0, 30):
            self.dieimages.append(theimage)

        #append the shells
        for i in range(0, 30):
            theshell = shell.shell2("picture/shell3.png", 10)
            self.shells.append(theshell)

        #reset
        self.reset()

    """reset function"""
    def reset(self):
        self.haveReleased = False
        self.walkindex = 0
        self.rect.center = (random.randrange(50, 500), -100)
        self.dying = False
        self.dieindex = 0
        self.live = 2
        if self.timeCount >= 900:
            self.stop = True

        

    """update function"""
    def update(self):

        #time count
        self.timeCount += 1
        
        if not self.stop:
            if self.timeCount == 900:
                self.dy -= 2

            #if it is not dying
            if not self.dying:

                #move down
                self.rect.centery += self.dy

                #rotate follow the mouse
                self.followMouse()
                self.rotate()

                #update the image
                self.walkindex += 1
                if self.walkindex > 9:
                    self.walkindex = 0
                self.rect.centery +=self.dy

                #if haveReleased is true, release shells
                if self.haveReleased:
                    self.release()
                #if not, random to set haveReleased true
                else:
                    if random.randrange(0, 20) == 0:
                        self.haveReleased = True
                #if out of screen, reset
                if self.rect.top > 540:
                    self.reset()

            #if it is dying
            else:
                #call die
                self.die()
                if self.timeCount >= 900:
                    self.dy = 0
                else:
                    self.rect.centery += 3
                    


    """followMouse function: change the rotate angle according to 
        the mouse position"""
    def followMouse(self):
        dx = pygame.mouse.get_pos()[0] - self.rect.centerx
        dy = pygame.mouse.get_pos()[1] - self.rect.centery

        dy *= -1
        radians = math.atan2(dy, dx)
        self.dir = radians * 180/math.pi + 90

    """rotate function: rotate the image"""
    def rotate(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.walkimages[self.walkindex], self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    """release function: release the shells, the shells is toward to the helicopter"""
    def release(self):
        self.rpause += 1
        if self.rpause == self.rdelay:

            radians = (self.dir - 90) * math.pi / 180

            #shell move speed and direction
            x = self.rect.centerx + math.cos(radians) * 30
            y = self.rect.centery - math.sin(radians) * 30

            #shell release
            self.shells[self.shellindex].release(self.dir, x, y)

            
            self.retimes += 1
            self.shellindex += 1

            if self.shellindex == 29:
                self.shellindex =0

            if self.retimes == 1:
                self.retimes = 0
                self.haveReleased = False
            self.rpause = 0

    """toExplode function: called while to die"""
    def toExplode(self):
        if not self.dying:
            self.sound.play()
        self.dying = True

    """die function: called while to dying"""
    def die(self):
        self.image = self.dieimages[self.dieindex]
        self.dieindex += 1
        if(self.dieindex > 39):
            self.reset()
