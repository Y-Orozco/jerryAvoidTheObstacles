# *** File: jerryAvoidTheObstacles-v3.py ***

# *** Author: Ysbelle Orozco ***

# *** Date: 3rd of June 2024 ***

import pygame
from pygame.locals import *

pygame.init()

#fps = 60
#fpsClock = pygame.time.Clock()

screenWidth = 800
screenHeight = 487
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
mouseGravity = 0
gameActive = False
startTime = 0
score = 0
#mouseRect = 0

TILE_WIDTH  = 16 #double tile height
TILE_WIDTH_HALF = TILE_WIDTH/2
TILE_HEIGHT = 8
TILE_HEIGHT_HALF = TILE_HEIGHT/2

def displayScore():
    currentTime = (pygame.time.get_ticks() // 100) - startTime
    scoreSurf = font.render(f'Score: {currentTime}', False, 'black')
    scoreRect = scoreSurf.get_rect(center = (490, 50))
    screen.blit(scoreSurf, scoreRect)
    return currentTime
#score is acting weird

backgroundSurf = pygame.transform.scale(pygame.image.load('graphics/isometricRoom2.png'), (800, 500))
backgroundRect = backgroundSurf.get_rect(topleft = (50, 0))

#loadCatSurf = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (200, 150)).convert_alpha()
#flipCatSurf = pygame.transform.flip(loadCatSurf, False, True)
#catSurf = pygame. transform.rotate(flipCatSurf, 180)
#catSurf.set_colorkey((0,0,0))
#catRect = catSurf.get_rect(bottomright = (175, 450))

class Player():
    def __init__(self,gridx,gridy):
        self.gridx = gridx
        self.gridy = gridy
        self.image = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
        self.x = (self.gridx-self.gridy)*TILE_WIDTH_HALF
        self.y = (self.gridx+self.gridy)*TILE_HEIGHT_HALF

    #def mouseRect(self, mouseRect):
        #mouseRect = 0
        #self.rect = self.image.get_rect(midbottom = (200, 300))
        #self.rect = mouseRect
        #return mouseRect 

    def update(self,udlr):
        u,d,l,r = udlr #extract key info
        if u:
            self.gridy -= 1
        elif d:
            self.gridy += 1
        elif l:
            self.gridx -= 1
        elif r:
            self.gridx += 1   
            
        self.x = (self.gridx-self.gridy)*TILE_WIDTH_HALF
        self.y = (self.gridx+self.gridy)*TILE_HEIGHT_HALF

        self.rect = self.image.get_rect(center = (self.x, self.y))
        
    def render(self,screen):
        self.rect = self.image.get_rect(center = (self.x, self.y))
        screen.blit(self.image, self.rect)

    #def jumping(mouseGravity):
    #    mouseGravity +=1
    #    mouseRect.y += mouseGravity
    #    if mouseRect.bottom >= 450:
    #        mouseRect.bottom = 450
    #    screen.blit(mouseSurf, mouseRect)
    #    return mouseGravity

mouseSurf = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
mousePlayer = Player(30,30)
#mouseRect = mouseSurf.get_rect(midbottom = (200, 450)) #ISSUE COLLISION

pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (75, 50))
pillowRect = pillowSurf.get_rect(bottomright = (800, 450))

gameMessage = font.render('COMPLETE THE GAME FOR JERRY TO GET HIS CHEESE', (False), ('white'))
gameMessageRect = gameMessage.get_rect(center =(490, 50))

gameInstruction = font.render('PRESS SPACEBAR TO PLAY', False, 'white')
gameInstructionRect = gameInstruction.get_rect(center = (490, 360))

mouseAndCat = pygame.transform.scale(pygame.image.load('graphics/menus/jerryAndTom.png'), (450, 215)).convert_alpha()
mouseAndCatRect = mouseAndCat.get_rect(center = (490, 200))

# REMEMBER ISSUE IS IMPORTING A SQUARE/RECT TO HIDE THE GAPE BETWEEN THE ROOM + WINDOW
#fillRoom = pygame.display.set_mode((400, 300))
#color = (237, 217, 147)

# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if gameActive: 
            if event.type == pygame.KEYDOWN: #RECT ->
                if event.key == pygame.K_SPACE:
                    mouseGravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                pillowRect.left = 980
                startTime = (pygame.time.get_ticks() // 100)

    if gameActive:

        screen.fill('white')
        screen.blit(backgroundSurf, backgroundRect)
        score = displayScore()
        #screen.blit(mouseSurf, mouseRect) #ISSUE HERE (COLLISION) DISPLAY
        
        #screen.blit(catSurf, catRect)

        #pygame.draw.rect(fillRoom, color, pygame.Rect(90, 90, 90, 90))

        pillowRect.x -= 8
        if pillowRect.right <= 0:
            pillowRect.left = 980
        screen.blit(pillowSurf, pillowRect)

        #RECT
        #mousePlayer.mouseRect(mouseRect)
        mousePlayer.render(screen)

        if mousePlayer.rect.colliderect(pillowRect):
            gameActive = False

        #if pillowRect.colliderect(mouseRect): #ISSUE COLLISION
        #    gameActive = False  

        inputs = pygame.key.get_pressed()

        #udlr -> up,down,left,right
        inputs_udlr = (inputs[K_UP],inputs[K_DOWN],inputs[K_LEFT],inputs[K_RIGHT])
        mousePlayer.update(inputs_udlr) #Update player with given udlr inputs
        #mousePlayer.render(screen) #Render player at screen with its x,y
        
        #mouseGravity +=1
        #mouseRect.y += mouseGravity
        #if mouseRect.bottom >= 450:
        #    mouseRect.bottom = 450
    
        if score == 500:
            gameactive = False

    else:
        if score == 0:
            screen.fill('white')
            screen.blit(mouseAndCat, mouseAndCatRect)
            screen.blit(gameMessage, gameInstructionRect)
            screen.blit(gameInstruction, gameInstructionRect)
        if score > 0 and score <= 499:
            screen.fill('white')
        if score > 0 and score == 500:
            screen.fill('yellow')

        #mousePlayer.jumping(mouseGravity)

        #somehow put the ability to jump in the Player class

    pygame.display.flip() #Update everything
    
    clock.tick(60)#Steady fps