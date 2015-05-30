"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Background.py
"""
import pygame
import random
import math
pygame.init()
pygame.mixer.init()

"""Background sprite: the background in the game"""
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/bg.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = 540
        self.rect.left = 0
        self.dy = 2
        self.timeCount = 0

    def update(self):
        #keep moving
        
        self.timeCount += 1
        if self.timeCount < 900:
            self.rect.centery += 3
            if self.rect.bottom >= 1740:
                self.rect.bottom = 540
