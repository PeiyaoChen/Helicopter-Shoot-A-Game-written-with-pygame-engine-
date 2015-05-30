"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Explode.py
"""
import pygame
import random
import math
import shell
import Helicopter
import Glow
pygame.init()
pygame.mixer.init()


"""sprite star"""
class Star(pygame.sprite.Sprite):

    """init function"""
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.timeCount = 0

        #load the image
        self.image = pygame.image.load("picture/star.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        #glow
        self.glow = Glow.Glow()
        
        #if the star exists in the screen, exist is true
        self.exist = False

        #move down speed 
        self.dy = 2

        self.sound = pygame.mixer.Sound("sound/getstar.ogg")
        self.sound.set_volume(4)

    """update function"""
    def update(self):
        
        self.timeCount += 1
        if self.timeCount >= 900:
            self.dy = 0
        self.glow.image = pygame.transform.scale(self.glow.image, (100, 100))
        self.glow.rect = self.glow.image.get_rect()
        self.glow.rect.center = self.rect.center
        self.rect.centery += self.dy
        if self.rect.top > 550:
            self.reset()

    """reset function"""
    def reset(self):
        self.rect.center = (3000, 3000)
        self.exist = False
        self.dy = 2

"""aid sprite"""
class Aid(pygame.sprite.Sprite):

    """init function"""
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.timeCount = 0

        #load the image
        self.image = pygame.image.load("picture/aid.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        #glow
        self.glow = Glow.Glow()
        self.exist = False
        
        #move down speed
        self.dy = 2

        self.sound = pygame.mixer.Sound("sound/aid.ogg")
        self.sound.set_volume(4)

    """update function"""
    def update(self):

        self.timeCount += 1
        if self.timeCount >= 900:
           self.dy = 0

        self.glow.image = pygame.transform.scale(self.glow.image, (100, 100))
        self.glow.rect = self.glow.image.get_rect()
        self.glow.rect.center = self.rect.center
        self.rect.centery += self.dy

        if self.rect.top > 550:
            self.reset()

    """reset function"""
    def reset(self):
        self.rect.center = (3000, 3000)
        self.exist = False
        self.dy = 2

"""explode sprite"""
class Explode(pygame.sprite.Sprite):

    """init function: size is the size of the explode"""
    def __init__(self, size):

        pygame.sprite.Sprite.__init__(self)

        self.sound = pygame.mixer.Sound("sound/explode.ogg")

        self.size = size
        
        #load the image
        self.image = pygame.image.load("picture/explode0.png")
        self.iamge = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        
        #explode image index
        self.index = 0

        self.havePlayed = False

        #image list
        self.imagelist = []

        #tell if to explode
        self.start = False

        #glow
        self.glow = Glow.Glow()
        self.glowIndex = 0
        self.rect.center = (-100, 100)
        self.glow.rect.center = self.rect.center

        #star
        self.star = Star()
        self.star.rect.center = (3000, 3000)

        #aid
        self.aid = Aid()
        self.aid.rect.center = (3000, 3000)
        self.reset()
        
    """"reset function"""
    def reset(self):
        for i in range(0, 23):
            theimage = pygame.image.load("picture/explode%d.png" %i)
            theimage = theimage.convert_alpha()
            theimage = pygame.transform.scale(theimage, (self.size, self.size))
            self.imagelist.append(theimage)
            self.havePlayed = False

    """update function"""
    def update(self):

        #set the glow position
        self.glow.rect.center = self.rect.center

        #if it start to explode
        if self.start:

            #randomly appear star
            if random.randrange(0, 50) == 0 and self.star.exist == False:
                self.star.exist = True
                self.star.rect.center = self.rect.center
            
            #randomly appear aid
            if random.randrange(0, 200) == 0 and self.aid.exist == False:
                self.aid.exist = True
                self.aid.rect.center = self.rect.center

            #change the image
            self.image = self.imagelist[self.index]
            self.index += 1


            self.glowIndex += 1
                
            if self.glowIndex < 12: 
                #increase the size of glow
                self.glow.image = pygame.transform.scale(self.glow.image, (30*self.glowIndex, 30*self.glowIndex))
                self.glow.rect = self.glow.image.get_rect()
                self.glow.rect.center = self.rect.center

            
            else:
                #reduce the size of glow
                self.glow.image = pygame.transform.scale(self.glow.image, (360 - 30 * (self.glowIndex - 12), \
                        360 - 30 * (self.glowIndex - 12)))
                self.glow.rect = self.glow.image.get_rect()
                self.glow.rect.center = self.rect.center

            #finish explode
            if(self.index == 23):
                self.index = 0
                self.start = False
                self.rect.center = (-200, -200)
                self.havePlayed = False
                self.glowIndex = 0
            

    """start_explode function: called when begin to explode"""
    def start_explode(self, x, y):
        if not self.havePlayed:
            self.sound.play()
            self.rect.center = (x, y)
            self.start = True
            self.havePlayed = True



