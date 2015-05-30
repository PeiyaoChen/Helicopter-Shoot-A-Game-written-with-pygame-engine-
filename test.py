"""Final Design
    Gmae name: helicopter shoot
    Author: Peiyao Chen
"""
import pygame
import random
pygame.init()
pygame.mixer.init()

class Shadow(pygame.sprite.Sprite):
    def __init__(self, picturename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picturename)
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 61))
        self.rect = self.image.get_rect()
    

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
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sound = pygame.mixer.Sound("sound/helishoot.ogg")
        self.image = pygame.image.load("picture/laser.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.dy = 20
        self.init()

    def init(self):
        self.rect.center = (-100, -100)

    def update(self):
        if self.rect.centery > -10:
            self.rect.centery -= self.dy

    def release(self, x, y):
        self.sound.play()
        self.rect.center = (x, y)
        
        
class Helicopter(pygame.sprite.Sprite):
    def __init__(self, propeller):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/helicopter.png")
        self.iamge = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.propeller = propeller
        self.lasers = []
        for i in range(0, 30):
            thelaser = Laser()
            self.lasers.append(thelaser)
        self.laserIndex = 0
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
        self.releaseDelay = 2
        self.releasePause = 0
        self.shadow = Shadow("picture/helishodw.png")
        
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
        self.shadow.rect.center = (self.rect.centerx - 20, self. rect.centery - 15)
        self.check_mouse()

    def check_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            self.releasePause += 1
            if self.releasePause >= self.releaseDelay:
                self.lasers[self.laserIndex].release(self.rect.centerx, self.rect.centery - 30)
                self.laserIndex += 1
                if(self.laserIndex >= 30):
                    self.laserIndex = 0
                self.releasePause = 0

class Fighter(pygame.sprite.Sprite):
    def __init__(self, propeller):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("picture/fighter.png")
        self.iamge = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.propeller = propeller
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
        self.shadow = HeliShadow("picture/figshadow.png")
        
        
    def update(self):
        self.propeller.rect.center = (self.rect.centerx + 2, self.rect.centery - 5)
        self.shadow.rect.center = (self.rect.centerx - 20, self. rect.centery - 15)
        self.check_mouse()


        
def main():
    screen = pygame.display.set_mode((720, 540))
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(False)
    
    clock = pygame.time.Clock()
    keepGoing = True
    propeller = Propeller()
    helicopter = Helicopter(propeller)
    friendSprites = pygame.sprite.OrderedUpdates(helicopter.shadow, helicopter, propeller, helicopter.lasers)
    while keepGoing:
        
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        friendSprites.clear(screen, background)
        friendSprites.update()
        friendSprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()

        
