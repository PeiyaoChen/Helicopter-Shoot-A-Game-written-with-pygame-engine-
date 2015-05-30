"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Propeller.py
"""
import pygame
import random
import math
pygame.init()
pygame.mixer.init()


"""Propeller sprite"""
class Propeller(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #load the image
        self.image = pygame.image.load("picture/luoxuan0.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        #image list
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
