"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Shadow.py
"""
import pygame
import random
import math
pygame.init()
pygame.mixer.init()

"""Sprite Shadow: the shadow of the fighter and helicopter"""
class Shadow(pygame.sprite.Sprite):
    def __init__(self, picturename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picturename)
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 61))
        
        self.imageMaster = self.image
        self.rect = self.image.get_rect()

    """rotate function"""
    def rotate(self, dir):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image, dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
    
    def reset(self):
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.rect.center = (3000, 3000)
