"""Final Design
    Gmae name: helicopter shooting
    Author: Peiyao Chen
"""

"""The main function of the Gmae"""

import pygame
import random
import math
import shell
import Helicopter
import Shadow
import Explode
import Fighter 
import Tank
import Propeller
import Artillery
import Boss
import Soldier
import Background
import Button
pygame.init()
pygame.mixer.init()


""" Function that change the color of the image to yellow
    While attacked, it will be called"""
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

"""Class of Label of text
show the text "Score", "Power" in the screen"""
class TextLabel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = "POWER"
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
    
    def update(self):
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.bottom = 530 


"""The Label to show the score number in the screen"""
class ScoreLabel(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = ""
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
    
    def update(self):
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.right = 710 
        self.rect.top = 10 

"""Function of Game State
    While enter the game state, it will be called"""
def Game():
    screen = pygame.display.set_mode((720, 540))

    #initialize the background
    background = Background.Background()

    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    keepGoing = True

    #initialize the power label
    powerLabel = TextLabel()

    #initialize the power rectangle of the boss
    powerRect = Boss.PowerRect((255, 0, 0), 3)

    #power to be added
    addpower = 0

    #propeller of helicopter
    propeller = Propeller.Propeller()

    #Helicopter
    helicopter = Helicopter.Helicopter(propeller)

    #list of fighters
    fighters = []

    #List of soldiers
    soldiers = []

    #List of  tanks
    tanks = []

    #List include all the shells of enemies
    shells = []

    #List of stars
    stars = []

    #List of aids
    aids = []

    #count the time the game state lasts after win
    winCount = 0
    #flag tell whether win
    winOut = False

    #count the time the game state lasts after lose
    loseCount = 0
    #flag tell whether lose
    loseOut = False

    #initialize the label of score 
    scoreLabel = ScoreLabel()
    #score number
    score = 0
    #set the score label text
    scoreLabel.text = "SCORE: %d" %score
    scoreLabel.rect.right = 710
    scoreLabel.rect.top = 10
    #the score will be added to
    toScore = 0
    
    #sprite group of background
    BGsprite = pygame.sprite.OrderedUpdates(background)

    #sprite group of enemies
    enemySprites = pygame.sprite.OrderedUpdates()
    
    #initialize the boss
    boss = Boss.Boss()
    
    #sprite group of boss
    BossSprite = pygame.sprite.OrderedUpdates(boss)
    BossSprite.add(boss.artilleryList)
    BossSprite.add(boss.explode.glow)
    BossSprite.add(boss.explodeList)
    BossSprite.add(boss.powerRect)
    
    #add the shells to the boss sprite group and
    #the list of shells
    for i in range(0, 5):
        BossSprite.add(boss.artilleryList[i].shells)
        shells.append(boss.artilleryList[i].shells)

    #List of boss
    bosses = [boss]

    #initialize the soldiers
    for i in range(0, 3):
        soldier = Soldier.Soldier()
        enemySprites.add(soldier)
        enemySprites.add(soldier.shells)
        soldiers.append(soldier)
        shells.append(soldier.shells)
        
    #initialize the tank appear from the left
    for i in range(0, 2):
        tank = Tank.Tank(0, 270 - 50*i, 100 + 50*i)
        enemySprites.add(tank.explode.star.glow)
        enemySprites.add(tank.explode.star)
        enemySprites.add(tank.explode.aid.glow)
        enemySprites.add(tank.explode.aid)
        enemySprites.add(tank)
        enemySprites.add(tank.artillery)
        enemySprites.add(tank.artillery.shells)
        enemySprites.add(tank.explode.glow)
        enemySprites.add(tank.explode)
        tanks.append(tank)
        shells.append(tank.artillery.shells)
        stars.append(tank.explode.star)
        aids.append(tank.explode.aid)

    #initialize the tanks appear from the right
    for i in range(0, 2):
        tank = Tank.Tank(1, 300 + 50*i, 100 + 50*i)
        enemySprites.add(tank.explode.star.glow)
        enemySprites.add(tank.explode.star)
        enemySprites.add(tank.explode.aid.glow)
        enemySprites.add(tank.explode.aid)
        enemySprites.add(tank)
        enemySprites.add(tank.artillery)
        enemySprites.add(tank.artillery.shells)
        enemySprites.add(tank.explode.glow)
        enemySprites.add(tank.explode)
        tanks.append(tank)
        shells.append(tank.artillery.shells)
        stars.append(tank.explode.star)
        aids.append(tank.explode.aid)

    #initialize the fighters
    for i in range(0, 2):
        fighter = Fighter.Fighter()
        enemySprites.add(fighter.shadow)
        enemySprites.add(fighter.explode.star.glow)
        enemySprites.add(fighter.explode.star)
        enemySprites.add(fighter.explode.aid.glow)
        enemySprites.add(fighter.explode.aid)
        enemySprites.add(fighter)
        enemySprites.add(fighter.propeller)
        enemySprites.add(fighter.lshells)
        enemySprites.add(fighter.rshells)
        enemySprites.add(fighter.explode.glow)
        enemySprites.add(fighter.explode)
        fighters.append(fighter)
        shells.append(fighter.lshells)
        shells.append(fighter.rshells)
        stars.append(fighter.explode.star)
        aids.append(fighter.explode.aid)
    

    #initialize the friend sprite group
    friendSprites = pygame.sprite.OrderedUpdates(powerLabel, powerRect, scoreLabel,\
            helicopter.shadow, helicopter, propeller, helicopter.lasers,\
             helicopter.explode.glow, helicopter.explode)
    #mouse initial position
    pygame.mouse.set_pos([360, 640])

    #game loop
    while keepGoing:
        
        clock.tick(30)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                return -1
        
        #examine whether the lasers collide fighters, tanks or bosses
        for thelaser in helicopter.lasers:
            attackEnemy = pygame.sprite.spritecollide(thelaser, fighters + tanks + bosses , False)
            if attackEnemy:
                thelaser.reset()
                for theEnemy in attackEnemy:
                    if(theEnemy.rect.bottom > 0):
                        theEnemy.attacked()
                        if theEnemy.live == 0:
                            theEnemy.toExplode()
        
        #examine whether the lasers collide soldiers 
        for thelaser in helicopter.lasers:
            attackEnemy = pygame.sprite.spritecollide(thelaser, soldiers, False)
            if attackEnemy:
                for theEnemy in attackEnemy:
                    if(theEnemy.rect.bottom > 0):
                        theEnemy.live -= 1
                        if theEnemy.live == 0:
                            theEnemy.toExplode()

        #examine whether the shells collide helicopter
        for i in range(0, len(shells)):
            heliAttacked = pygame.sprite.spritecollide(helicopter, shells[i], False)
            if heliAttacked:
                for theshell in heliAttacked:
                    dx = helicopter.rect.centerx - theshell.rect.centerx
                    dy = helicopter.rect.centery - theshell.rect.centery
                    dis = math.sqrt(dx * dx +  dy * dy)
                    if dis < 30 and theshell.rect.top < 540:
                        theshell.reset()
                        helicopter.attacked()
                        helicopter.live -= 1
                        powerRect.power = helicopter.live
                        if helicopter.live == 0:
                            helicopter.toExplode()

        #examine whether the helicopter collide stars
        hitStar = pygame.sprite.spritecollide(helicopter, stars, False)
        if hitStar:
            #if colliding a star, score increases 100
            for thestar in hitStar:
                toScore += 100 
                thestar.sound.play()
                thestar.reset()

        #socre increase by 2 once,and constantly until increasing 100
        if score < toScore:
            score += 2 
            scoreLabel.text = "Score: %d" %score


        #examine whether the helicopter collides aids
        hitAid = pygame.sprite.spritecollide(helicopter, aids, False)
        if hitAid:
            for theAid in hitAid:
                theAid.sound.play()
                addpower += 20
                theAid.reset()
            
        #if addpower is more than 0, live will increase
        if addpower > 0:
            if helicopter.live == 30:
                addpower = 0
            else:
                addpower -= 1
                helicopter.live += 1
                powerRect.power = helicopter.live

        #if helicopter's live is zero, game lose
        if helicopter.live == 0:
            loseOut = True
        
        #if boss's live is zero ,game win
        if boss.live == 0:
            winOut = True 

        #After 90 frame since game lose,get out of the game state
        if loseOut:
            loseCount += 1
            if loseCount == 90:
                return -2
        

        #After 90 frame since game win,get out of the game state
        if winOut:
            winCount += 1
            if winCount == 90:
                return score
        
        #sprites update
        BGsprite.update()
        BGsprite.draw(screen)
        enemySprites.update()
        enemySprites.draw(screen)
        
        #After 900 frames(30 second) the boss will appears
        if background.timeCount > 900:
            BossSprite.update()
            BossSprite.draw(screen)
            
            
        friendSprites.update()
        friendSprites.draw(screen)

        #screen refresh
        pygame.display.flip()
        

"""Class shows the Loading text """
class Text(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 40)
        self.text = "Loading..."
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (360, 216)

    def update(self):
        self.image = self.font.render(self.text, 1, (255, 255, 255))

"""Class that show the image,
    Used to show the some texts whose type are images"""
class ImageShow(pygame.sprite.Sprite):
    def __init__(self, picture):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

"""Funtion of Etrance State"""
"""The function show the beginning screen of the game,
    including the menu."""
def Entrance():
    #sound while click the button
    sound = pygame.mixer.Sound("sound/buttonpress.ogg")
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((720, 540))

    #Entrance screen background
    background = pygame.image.load("picture/entrance/EntranceBG.png")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #initialize the buttons
    PlayGame = Button.Button("picture/entrance/PlayGame1.png", "picture/entrance/PlayGame2.png", True, (360, 266), 1)
    HowToPlay = Button.Button("picture/entrance/HowToPlay1.png", "picture/entrance/HowToPlay2.png", True, (360, 346), 0)
    About = Button.Button("picture/entrance/About1.png", "picture/entrance/About2.png", True, (360, 426), 1)

    #Menu sprite group
    MenuSprites = pygame.sprite.OrderedUpdates(PlayGame, HowToPlay, About)

    #loading text
    loadingText = Text()
    LoadingSprite = pygame.sprite.OrderedUpdates(loadingText)
    

    KeepGoing = True

    clock = pygame.time.Clock()

    #loop
    while KeepGoing:
        
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeepGoing = False
                return -1
            
            #if mouse button up
            elif event.type == pygame.MOUSEBUTTONUP:
                # if the cursor is on the button "play game"
                if PlayGame.IsOn:
                    sound.play()
                    MenuSprites.clear(screen, background)
                    LoadingSprite.update()
                    MenuSprites.update()
                    LoadingSprite.draw(screen)
                    MenuSprites.draw(screen)
                    pygame.display.flip()
                    return 1

                # if the cursor is on the button "How to play"
                elif HowToPlay.IsOn:
                    sound.play()
                    return 2

                # if the cursor is on the button "How to play"
                elif About.IsOn:
                    sound.play()
                    return 3
                    
        #sprite update
        MenuSprites.clear(screen, background)
        MenuSprites.update()
        MenuSprites.draw(screen)

        #screen refreshes 
        pygame.display.flip()

    return 0

"""The Instruction State function.
    It shows you the screen that teach you
    how to play the game"""
def Instruction():

    sound = pygame.mixer.Sound("sound/buttonpress.ogg")
    screen = pygame.display.set_mode((720, 540))
    background = pygame.image.load("picture/entrance/EntranceBG.png")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    back = Button.Button("picture/entrance/back1.png", "picture/entrance/back2.png", False, (700, 520))
    back.rect.right = 700
    back.rect.bottom = 520

    #initialize the instruction text sprite
    InstructionState = ImageShow("picture/entrance/Instruction.png")
    InstructionState.rect.center = (300, 300)

    InstructionSprites = pygame.sprite.OrderedUpdates(back, InstructionState)

    KeepGoing = True

    clock = pygame.time.Clock()

    while KeepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeepGoging = False
                return -1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if back.IsOn:
                    sound.play()
                    KeepGoing = False
                    return 0

        #sprite updates
        InstructionSprites.clear(screen, background)
        InstructionSprites.update()
        InstructionSprites.draw(screen)
        #fresh screen
        pygame.display.flip()
        
        


    
"""Function of about state.
    It shows you something about the game."""
def About():
    
    sound = pygame.mixer.Sound("sound/buttonpress.ogg")
    screen = pygame.display.set_mode((720, 540))
    background = pygame.image.load("picture/entrance/EntranceBG.png")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #back button
    back = Button.Button("picture/entrance/back1.png", "picture/entrance/back2.png", False, (700, 520))
    back.rect.right = 700
    back.rect.bottom = 520

    #about text sprite
    AboutState = ImageShow("picture/entrance/AboutState.png")
    AboutState.rect.center = (300, 300)

    AboutSprites = pygame.sprite.OrderedUpdates(back, AboutState)

    KeepGoing = True

    clock = pygame.time.Clock()

    while KeepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeepGoging = False
                return -1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if back.IsOn:
                    sound.play()
                    KeepGoing = False
                    return 0

        #sprite updates
        AboutSprites.clear(screen, background)
        AboutSprites.update()
        AboutSprites.draw(screen)
        #screen fresh
        pygame.display.flip()
        
        
"""The function of win State.
    When you win the game, it will be called"""
def win(score):

    sound = pygame.mixer.Sound("sound/buttonpress.ogg")
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((720, 540))

    #win background
    background = pygame.image.load("picture/win/WinBG.jpg")
    background = background.convert()

    #score text
    font = pygame.font.SysFont("None", 50)
    scoreLabel = font.render(str(score), 1, (0, 0, 0))
    background.blit(scoreLabel, (225, 378))
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #"menu" button
    menu = Button.Button("picture/win/menu1.png", "picture/win/menu2.png", False, (700, 520))
    menu.rect.right = 700
    menu.rect.bottom = 520

    #sprite group
    AboutSprites = pygame.sprite.OrderedUpdates(menu)

    KeepGoing = True

    clock = pygame.time.Clock()

    while KeepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeepGoging = False
                return -1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if menu.IsOn:
                    sound.play()
                    KeepGoing = False
                    return 0

        #sprite updates
        AboutSprites.clear(screen, background)
        AboutSprites.update()
        AboutSprites.draw(screen)

        #screeen refresh
        pygame.display.flip()
        


"""The function of lose state.
    when you lose the game,it will be called"""
def lose():
    sound = pygame.mixer.Sound("sound/buttonpress.ogg")
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((720, 540))

    #the lose background
    background = pygame.image.load("picture/lose/LoseBG.jpg")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #"menu" button
    menu = Button.Button("picture/lose/menu1.png", "picture/lose/menu2.png", False, (700, 520))
    menu.rect.right = 700
    menu.rect.bottom = 520

    AboutSprites = pygame.sprite.OrderedUpdates(menu)

    KeepGoing = True

    clock = pygame.time.Clock()

    while KeepGoing:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeepGoging = False
                return -1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if menu.IsOn:
                    sound.play()
                    KeepGoing = False
                    return 0

        #sprite upsdates
        AboutSprites.clear(screen, background)
        AboutSprites.update()
        AboutSprites.draw(screen)
        #screen refresh
        pygame.display.flip()
        

"""Main function"""    
def main():
    KeepGoing = True
    while KeepGoing:
        
        #enterance background music
        bgmusic = pygame.mixer.music.load("sound/DARK_KNIGHT.ogg")
        pygame.mixer.music.play(-1)

        #call enterance function
        EntranceResult = Entrance()

        #if EntranceResult is 1, call Gmae function
        if EntranceResult == 1:
            pygame.mixer.music.stop()
            gamemusic = pygame.mixer.Sound("sound/GameBG.ogg")
            gamemusic.play(-1)
            GameResult = Game()
            #if GameResult is -1, exit
            if GameResult == -1:
                KeepGoing = False

            #if GameResult is -2, lose
            elif GameResult == -2:
                #call lose function
                LoseResult = lose()
                gamemusic.stop() 
                if LoseResult == -1:
                    KeepGoing = False
            #if gameResult is more than 0, win and the value
            #is the score
            elif GameResult >= 0 :
                #call win function
                WinResult = win(GameResult)
                gamemusic.stop()
                if WinResult == -1:
                    KeepGoing = False
                
        #if EntranceResult is 2, call Instruction function
        elif EntranceResult == 2:
            InstructionResult = Instruction()
            if InstructionResult == -1:
                KeepGoing = False

        #if EntranceResult is 3, call About function
        elif EntranceResult == 3:
            AboutResult = About()
            if AboutResult == -1:
                KeepGoing = False
        
        #if EntranceResult is -1, exit
        elif EntranceResult == -1:
            KeepGoing = False



if __name__ == "__main__":
    main()

