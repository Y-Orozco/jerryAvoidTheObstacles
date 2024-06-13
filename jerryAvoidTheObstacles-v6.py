# *** File: tomAndJerryCheeseRace-v6.py ***

# *** Author: Ysbelle Orozco ***

# *** Date: 7th of June 2024 ***

import pygame
from pygame.locals import *

pygame.init()

screenWidth = 800
screenHeight = 487
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
mouseGravity = 0
gameActive = False
startTime = 0
score = 0
helpScreen = False

TILE_WIDTH  = 16 #double tile height
TILE_WIDTH_HALF = TILE_WIDTH/2
TILE_HEIGHT = 6
TILE_HEIGHT_HALF = TILE_HEIGHT/2

pygame.display.set_caption('Tom and Jerry Cheese Race')

backgroundSurf = pygame.transform.scale(pygame.image.load('graphics/isometricRoom2.png'), (800, 510))
backgroundRect = backgroundSurf.get_rect(topleft = (50, 2))

pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (75, 50))
pillowRect = pillowSurf.get_rect(center = (800, 487))

gameMessage = font.render('COMPLETE THE GAME FOR JERRY TO GET HIS CHEESE', (False), ('black'))
gameMessageRect = gameMessage.get_rect(center =(400, 50))

gameInstruction = font.render('PRESS SPACEBAR TO PLAY', False, 'black')
gameInstructionRect = gameInstruction.get_rect(center = (400, 360))

mouseAndCat = pygame.transform.scale(pygame.image.load('graphics/menus/jerryAndTom.png'), (450, 215)).convert_alpha()
mouseAndCatRect = mouseAndCat.get_rect(center = (400, 190))

buttonSurf = pygame.Surface((150, 50))
buttonRect = pygame.Rect(300, 400, 500, 500)
buttonText = font.render('Click Me', True, ('black'))
buttonTextRect = buttonText.get_rect(center = (buttonSurf.get_width()/2, buttonSurf.get_height()/2))

class Player():
    def __init__(self,gridx,gridy):
        self.gridx = gridx
        self.gridy = gridy
        self.mouseSurf1 = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
        self.mouseSurf2 = pygame.transform.scale(pygame.image.load('graphics/Player/2.png'), (100, 75)).convert_alpha()
        self.mouseSurf3 = pygame.transform.scale(pygame.image.load('graphics/Player/3.png'), (100, 75)).convert_alpha()
        self.mouseSurf4 = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (100, 75)).convert_alpha()
        self.mouseWalk = [self.mouseSurf1, self.mouseSurf2, self.mouseSurf3, self.mouseSurf4]
        self.mouseIndex = 0
        self.image = self.mouseWalk[self.mouseIndex]
        self.x = (self.gridx-self.gridy)*TILE_WIDTH_HALF
        self.y = (self.gridx+self.gridy)*TILE_HEIGHT_HALF

    def animationState(self):
        self.mouseIndex += 0.1
        if self.mouseIndex >= len(self.mouseWalk):
            self.mouseIndex = 0
        self.image = self.mouseWalk[int(self.mouseIndex)]

    def update(self, udlr):
        u,d,l,r = udlr #extract key info
        #u,d = ud
        #self.move = True
        if self.move:
            if u:
                self.gridy -= 1
            elif d:
                self.gridy += 1
            elif l:
                self.gridx -= 1
            elif r:
                self.gridx += 1   
        else:
            self.move=False
            print('No moving')
            if self.rect.right >=700:
                if d:
                    self.gridy += 1
            if self.rect.left <=50:
                if u: 
                    self.gridy -=1
            if self.rect.top <=120:
                #if u: 
                #    self.gridy -=1
                #if d:
                #    self.gridy += 1
                if r:
                    self.gridx +=1
        self.x = (self.gridx-self.gridy)*TILE_WIDTH_HALF
        self.y = (self.gridx+self.gridy)*TILE_HEIGHT_HALF

        self.rect = self.image.get_rect(center = (self.x, self.y))

    def render(self,screen):
        self.animationState()
        self.rect = self.image.get_rect(center = (self.x + 125, self.y + 195))
        self.move = True
        screen.blit(self.image, self.rect)

        if self.rect.left <= 50: 
            self.move = False
            print('Left')
        if self.rect.right >= 700:
            self.move = False
            print('Right')
        if self.rect.top <=120:
            self.move = False
            print('Top')

mouseSurf = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
mousePlayer = Player(30,30)

def displayScore():
    currentTime = (pygame.time.get_ticks() // 100) - startTime
    scoreSurf = font.render(f'Score: {currentTime}', False, 'black')
    scoreRect = scoreSurf.get_rect(center = (130, 75))
    screen.blit(scoreSurf, scoreRect)
    return currentTime

def helpInstructions():
    help = font.render('USE UP, DOWN, LEFT AND ARROW KEYS', (False), ('black'))
    help1 = font.render('TO MOVE JERRY AWAY FROM THE OBSTACLES', (False), ('black'))
    helpRect =  help.get_rect(center = (400, 150))

    screen.blit(help, helpRect)
    screen.blit(help1, (130, 170))

    if buttonRect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(buttonSurf, (127, 255, 212), (1, 1, 148, 48))
    else:
        pygame.draw.rect(buttonSurf, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(buttonSurf, (255, 255, 255), (1, 1, 148, 48))
        pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 1, 148, 1), 2)
        pygame.draw.rect(buttonSurf, (0, 100, 0), (1, 48, 148, 10), 2)

    buttonSurf.blit(buttonText, buttonTextRect)
    screen.blit(buttonSurf, buttonRect)

def homePage():
    if score == 0:
        screen.fill('white')
        if buttonRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(buttonSurf, (127, 255, 212), (1, 1, 148, 48))
        else:
            pygame.draw.rect(buttonSurf, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(buttonSurf, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(buttonSurf, (0, 100, 0), (1, 48, 148, 10), 2)

        buttonSurf.blit(buttonText, buttonTextRect)
        screen.blit(buttonSurf, buttonRect)

        screen.blit(mouseAndCat, mouseAndCatRect)
        screen.blit(gameMessage, gameMessageRect)
        screen.blit(gameInstruction, gameInstructionRect)

def playAgainPage():
    if score > 0 and score <= 499:
        screen.fill('white')
        scoreMessage = font.render(f'Your score: {score}', False, ('black'))
        scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
        screen.blit(scoreMessage, scoreMessageRect)
        screen.blit(mouseAndCat, mouseAndCatRect)

def endPage():
    if score > 0 and score == 500:
        screen.fill('white')
        scoreMessage = font.render(f'JERRY CAN GET HIS CHEESE', False, ('black'))
        scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
        screen.blit(scoreMessage, scoreMessageRect)
        screen.blit(mouseAndCat, mouseAndCatRect)

def game(gameOn, scored):      
        screen.fill('white')
        pygame.draw.line(screen, ('black'), (0,437), (800, 145), 5)
        screen.blit(backgroundSurf, backgroundRect)
        pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(320,320,800,210))
        pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(700, 300, 100, 20))
        screen.blit(pillowSurf, pillowRect)
        
        scored = displayScore()

        pillowRect.x -=10
        pillowRect.y -=1 
        if pillowRect.right <= 0:
            pillowRect.bottom = 487
            pillowRect.left = 800

        mousePlayer.render(screen)

        if mousePlayer.rect.colliderect(pillowRect) or scored == 500:
            gameOn = False

        inputs = pygame.key.get_pressed()

        #udlr -> Up, Down, Left and Right
        inputs_udlr = (inputs[K_UP],inputs[K_DOWN],inputs[K_LEFT],inputs[K_RIGHT])
        mousePlayer.update(inputs_udlr) #Update player with given udlr input

        print(score)
        return gameOn, scored

# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameActive:
            gameActive = True
            helpScreen = False
            pillowRect.bottom = 487
            pillowRect.left = 800
            startTime = (pygame.time.get_ticks() // 100)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not gameActive:
                print('Going to Help Screen')
                helpScreen = True


    if gameActive:

        gameActive, score = game(gameActive, score)

    if helpScreen:
        helpInstructions()

    if not gameActive and not helpScreen:
        homePage()
        playAgainPage()
        endPage()

    pygame.display.flip() #Update everything
    
    clock.tick(60) #Steady fps