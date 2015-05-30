"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Glow.py
"""
import pygame
import random
import math
import Explode
pygame.init()
pygame.mixer.init()

"""Glow sprite"""
class Glow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/glow.png")

        #set the alpha of the image at 0.5
        for col in range(0, self.image.get_width()):
            for row in range(0, self.image.get_height()):
                (r, g, b, a) = self.image.get_at((col, row))
                self.image.set_at((col, row), (r, g, b, int(0.5 * a)))

        self.image = self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
