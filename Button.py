"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
    Module: Button.py
"""



import pygame
import random
import math
pygame.init()
pygame.mixer.init()

"""Button sprite: the buttons in the game"""
class Button(pygame.sprite.Sprite):

    """init fuction: pictureNotOn is the name of picture the cursor not on,
        pictureOn is the name of picture the cursor on, isMenu tell whether
        the button is the menu button(Menu button will move to the center
        when enter the Entrance state screen), dir is the moving direction
        """
    def __init__(self, pictureNotOn, pictureOn, isMenu, position, dir = 0):

        pygame.sprite.Sprite.__init__(self)

        #image of button cursor not on
        self.imageNotOn = pygame.image.load(pictureNotOn)
        self.imageNotOn = self.imageNotOn.convert_alpha()

        #image of button cursor on
        self.imageOn = pygame.image.load(pictureOn)
        self.imageOn = self.imageOn.convert_alpha()

        #initialize the original image
        self.image = self.imageNotOn
        self.rect = self.image.get_rect()

        #move
        #move to right
        if dir == 1:
            self.dx = 80 
            self.rect.center = (-200, position[1])

        #move to left
        else:
            self.dx = -80
            self.rect.center = (920, position[1])



        
        self.oldscale = self.imageNotOn.get_size()
        self.oldcenter =  position
        self.index = 30
        
    
        self.IsOn = False
        self.isMenu = isMenu 
        self.haveMoved = False
        
        #if it is the menu button, when cursor is on it ,it will
        #play sound
        if self.isMenu:
            self.sound = pygame.mixer.Sound("sound/button.ogg")
        self.soundHavePlayed = False

    def update(self):

        if (not self.haveMoved) and self.isMenu:

            #move to the center
            self.rect.centerx += self.dx

            if self.rect.centerx == 360:
                self.haveMoved = True
        
        else:

            (mousex, mousey) = pygame.mouse.get_pos()
            
            #if the cursor is on the image of the button
            if mousex > self.rect.left and mousex < self.rect.right \
                    and mousey > self.rect.top and mousey < self.rect.bottom:

                        if self.isMenu:
                            if self.soundHavePlayed == False:
                                self.sound.play()
                                self.soundHavePlayed = True

                        self.image = self.imageOn
                        #set IsOn true
                        self.IsOn = True

            #if the cursor is not on the image of button
            else:
                self.image = self.imageNotOn
                self.IsOn = False
                self.soundHavePlayed = False
