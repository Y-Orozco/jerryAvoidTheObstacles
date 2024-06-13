# *** File: jerryAvoidTheObstacles-v2.py ***

# *** Author: Ysbelle Orozco ***

# *** Date: 29th of May 2024 ***

import pygame
from sys import exit

pygame.init()

screenWidth = 980
screenHeight = 487

screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption('Tom and Jerry Cheese Race')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50) #font type, font size
mouseGravity = 0   
gameActive = False  
startTime = 0
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mouseSurf1 = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
        mouseSurf2 = pygame.transform.scale(pygame.image.load('graphics/Player/2.png'), (100, 75)).convert_alpha()
        mouseSurf3 = pygame.transform.scale(pygame.image.load('graphics/Player/3.png'), (100, 75)).convert_alpha()
        mouseSurf4 = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (100, 75)).convert_alpha()
        self.mouseWalk = [mouseSurf1, mouseSurf2, mouseSurf3, mouseSurf4]
        self.mouseIndex = 0
        self.image = self.mouseWalk[self.mouseIndex]
        #pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 450:
            self.rect.bottom = 450

    def animationState(self):
        self.mouseIndex += 0.1
        if self.mouseIndex >= len(self.mouseWalk):
            self.mouseIndex = 0
        self.image = self.mouseWalk[int(self.mouseIndex)]

    def update(self):
        self.playerInput()
        self.applyGravity()
        self.animationState()

def displayScore():
    currentTime = (pygame.time.get_ticks() // 100) - startTime
    scoreSurf = font.render(f'Score: {currentTime}', False, 'black')
    scoreRect = scoreSurf.get_rect(center = (490, 50))
    screen.blit(scoreSurf, scoreRect)
    return currentTime

def playerAnimation():
    #play walking animation when player is on floor
    global mouseSurf, mouseIndex

    mouseIndex += 0.1
    if mouseIndex >= len(mouseWalk):
        mouseIndex = 0
    mouseSurf = mouseWalk[int(mouseIndex)]

backgroundSurf = pygame.image.load('graphics/bedroom.png').convert()

mouseSurf1 = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
mouseSurf2 = pygame.transform.scale(pygame.image.load('graphics/Player/2.png'), (100, 75)).convert_alpha()
mouseSurf3 = pygame.transform.scale(pygame.image.load('graphics/Player/3.png'), (100, 75)).convert_alpha()
mouseSurf4 = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (100, 75)).convert_alpha()
mouseWalk = [mouseSurf1, mouseSurf2, mouseSurf3, mouseSurf4]
mouseIndex = 0

mouseSurf = mouseWalk[mouseIndex]
mouseRect = mouseSurf.get_rect(midbottom = (360, 450))

player = pygame.sprite.GroupSingle()
player.add(Player())

loadCatSurf = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (200, 150)).convert_alpha()
flipCatSurf = pygame.transform.flip(loadCatSurf, False, True)
catSurf = pygame. transform.rotate(flipCatSurf, 180)
catSurf.set_colorkey((0,0,0))
catRect = catSurf.get_rect(bottomright = (175, 450))

pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (75, 50))                                                                                                                                           
pillowRect = pillowSurf.get_rect(bottomright = (900, 450))

#menu screens
gameMessage = font.render('COMPLETE THE GAME FOR JERRY TO GET HIS CHEESE', (False), ('black'))
gameMesageRect = gameMessage.get_rect(center = (490, 50))

gameInstruction = font.render('PRESS SPACEBAR TO PLAY', False, 'black')
gameInstructionRect = gameInstruction.get_rect(center = (490, 360))

mouseAndCat = pygame.transform.scale(pygame.image.load('graphics/menus/jerryAndTom.png'), (450, 215)).convert_alpha()
mouseAndCatRect = mouseAndCat.get_rect(center = (490, 200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and mouseRect.bottom >= 450:
                    mouseGravity = -20
        else:      
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                pillowRect.left = 980
                startTime = (pygame.time.get_ticks() // 100)

    if gameActive: 
        screen.blit(backgroundSurf, (0, 0))
        
        #mouse
        mouseGravity +=1
        mouseRect.y += mouseGravity

        if mouseRect.bottom >= 450:
            mouseRect.bottom = 450
        playerAnimation()
        screen.blit(mouseSurf, mouseRect)

        
        player.draw(screen)
        player.update()

        screen.blit(catSurf, catRect)

        pillowRect.x -= 8
        if pillowRect.right <= 0:
            pillowRect.left = 980
        screen.blit(pillowSurf, pillowRect)

        #collison
        if pillowRect.colliderect(mouseRect):
            gameActive = False
        
        score = displayScore()

        if score == 500:
            gameActive = False
    
    else:        
        if score == 0:
            screen.fill('white')
            screen.blit(mouseAndCat, mouseAndCatRect)
            screen.blit(gameMessage, gameMesageRect)
            screen.blit(gameInstruction, gameInstructionRect)
        if score > 0 and score <= 499:
            screen.fill('white')
            scoreMessage = font.render(f'Your score: {score}', False, ('black'))
            scoreMessageRect = scoreMessage.get_rect(center = (490, 50))
            screen.blit(scoreMessage, scoreMessageRect)
            screen.blit(gameInstruction, (100, 100))
        if score > 0 and score == 500:
            screen.fill('yellow')

    pygame.display.update()
    clock.tick(60)