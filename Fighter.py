"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Fighter
"""
import pygame
import random
import math
import shell
import Helicopter
import Shadow
import Explode
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

"""propeller sprite """
class Propeller(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/luoxuan0.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.imagelist = []
        self.index = 0
        self.reset()

    def reset(self):
        for i in range(0, 8):
            theImage = pygame.image.load("picture/luoxuan%d.png" %i)
            theImage = theImage.convert_alpha()
            self.imagelist.append(theImage)

    def update(self):
        self.image = self.imagelist[self.index]
        self.index += 1
        if self.index > 7:
            self.index = 0

"""Fighter sprite"""
class Fighter(pygame.sprite.Sprite):
    
    """init function"""
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.timeCount = 0
        self.stop = False

        #normal image
        self.imageMaster = pygame.image.load("picture/fighter.png")
        self.iamgeMaster = self.imageMaster.convert_alpha()


        #image while attacked
        self.imageAttacked = pygame.image.load("picture/fighter.png")
        self.imageAttacked = self.imageAttacked.convert_alpha()
        self.imageAttacked = changeColor(self.imageAttacked)

        self.image = self.imageMaster
        self.rect = self.image.get_rect()

        #propeller
        self.propeller = Propeller()
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
        
        #shadow
        self.shadow = Shadow.Shadow("picture/figshadow.png")

        #explode
        self.explode = Explode.Explode(100)

        #speed in y coordinate
        self.dy = 4

        #releasing shells's times
        self.retimes = 0

        #left shells
        self.lshells = []
        #right shells
        self.rshells = []

        
        self.rindex = 0

        #delay 
        self.delay = 16 
        self.pause = 0

        #flag to tell if it is destroyed
        self.destroyed = False

        #rotate times, used while being destroyed
        self.rotatetimes = 0

        #live
        self.live = 3

        #tell whether it is being attacked
        self.beattacked = False
        self.attackedIndex = 0

        #the shell list 
        for i in range(0, 30):
            thershell = shell.shell1(1)
            self.rshells.append(thershell)
            thelshell = shell.shell1(0)
            self.lshells.append(thelshell)
        
        self.reset()

    """update function"""
    def update(self):
        
        #time count
        self.timeCount += 1

        #if stop is not true
        if not self.stop:

            #if time count is 900
            if self.timeCount == 900:
                self.dy -= 2

            #if it has not been destroyed
            if not self.destroyed:

                #if it is being attacked
                if self.beattacked:
                    if (self.attackedIndex / 2  ) % 2 == 0:
                        self.image = self.imageAttacked
                    else:
                        self.image = self.imageMaster
                    self.attackedIndex += 1
                    if self.attackedIndex > 20:
                        self.attackedIndex = 0
                        self.beattacked = False
                        self.image = self.imageMaster
                        
                #propeller's position
                self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery + 10)

                #shadow's postion
                self.shadow.rect.center = (self.rect.centerx - 20, self. rect.centery - 15)

                #move down
                self.rect.centery += self.dy

                #release shells
                if self.retimes != 0:
                    self.pause += 1
                    if self.pause == self.delay:
                        self.rshells[self.rindex].release(self.rect.centerx + 10, self.rect.centery + 15)
                        self.lshells[self.rindex].release(self.rect.centerx - 10, self.rect.centery + 15)
                        self.retimes += 1
                        if self.retimes >= 5:
                            self.retimes = 0
                        self.rindex += 1
                        if self.rindex >= 30:
                            self.rindex = 0
                        self.pause = 0
                else:
                    #release shells randomly
                    release = random.randrange(0, 100)
                    if release == 0:
                        self.retimes = 1
                    

                #if it is out of the screen, reset.
                if self.rect.centery > 600:
                    self.reset()

            #if it is being destroyed
            else:
                oldcenter = self.rect.center

                #rotate the body and shadow
                self.image = pygame.transform.rotate(self.image, 5)
                self.rect = self.image.get_rect()
                self.rect.center = oldcenter
                self.shadow.rotate(5)
                self.rotatetimes += 1

                if(self.rotatetimes == 15):
                    self.rotatetimes = 0
                    oldcenter = self.rect.center
                    self.image = pygame.transform.rotate(self.image, -75)
                    self.rect = self.image.get_rect()
                    self.rect.center = oldcenter
                    self.reset()
                
    """reset function"""
    def reset(self):
        self.image = self.imageMaster
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, 720)
        self.rect.centery = -100
        self.shadow.reset()
        
        self.destroyed = False
        self.live = 3
        self.beattacked = False
        self.attackedIndex = 0
        if self.timeCount >= 900:
            self.stop = True

    """toExplode function: called when to explode"""
    def toExplode(self):
        self.explode.start_explode(self.rect.centerx, self.rect.centery)
        self.propeller.rect.center = (-1000, -1000)
        self.destroyed = True

    """attacked function: callsed when attacked"""
    def attacked(self):
        self.beattacked = True
        self.live -= 1
