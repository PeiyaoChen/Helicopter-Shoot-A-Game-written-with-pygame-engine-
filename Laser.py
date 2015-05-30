"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Laser.py
"""
import pygame
import random
import math
pygame.init()
pygame.mixer.init()


"""Laser sprite: the laser which released by helicopter"""
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #sound
        self.sound = pygame.mixer.Sound("sound/helishoot.ogg")
        self.sound.set_volume(0.5)

        #image
        self.image = pygame.image.load("picture/laser.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        #move speed
        self.dy = 20
        self.reset()


    def update(self):
        if self.rect.bottom > 0:
            #move up
            self.rect.centery -= self.dy
        else:
            self.reset()

    """release function: release laser at the position (x, y)"""
    def release(self, x, y):
        self.sound.play()
        self.rect.center = (x, y)

    def reset(self):
        self.rect.center = (-2000, -2000)
