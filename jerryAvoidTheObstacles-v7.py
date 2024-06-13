# *** File: jerryAvoidTheObstacles-v7.py ***

# *** Author: Ysbelle Orozco ***

# *** Date: 8th of June 2024 ***

import pygame
from pygame.locals import *
from random import randint

pygame.init()

screenWidth = 800
screenHeight = 487
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
gameStart = False
gameActive = False
startTime = 0
score = 0
helpScreen = False
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1200)
tileWidth  = 16 #double tile height
tileWidthHalf = tileWidth/2
tileHeight = 6
tileHeightHalf = tileHeight/2

pygame.display.set_caption('Tom and Jerry Cheese Race')

#Main Character Class
class Player(pygame.sprite.Sprite):
    def __init__(self,gridx,gridy):
        #ADD TO DATA DICTIONARY
        self.gridx = gridx
        self.gridy = gridy
        self.mouseSurf1 = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
        self.mouseSurf2 = pygame.transform.scale(pygame.image.load('graphics/Player/2.png'), (100, 75)).convert_alpha()
        self.mouseSurf3 = pygame.transform.scale(pygame.image.load('graphics/Player/3.png'), (100, 75)).convert_alpha()
        self.mouseSurf4 = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (100, 75)).convert_alpha()
        self.mouseWalk = [self.mouseSurf1, self.mouseSurf2, self.mouseSurf3, self.mouseSurf4]
        self.mouseIndex = 0
        self.image = self.mouseWalk[self.mouseIndex]
        self.x = (self.gridx-self.gridy)*tileWidthHalf
        self.y = (self.gridx+self.gridy)*tileHeightHalf

    def animationState(self):
        #ADD TO DATA DICTIONARY
        self.mouseIndex += 0.1
        if self.mouseIndex >= len(self.mouseWalk):
            self.mouseIndex = 0
        self.image = self.mouseWalk[int(self.mouseIndex)]

    def update(self, udlr):
        u,d,l,r = udlr #extract key info
        #ADD TO DATA DICTIONARY
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
            if self.rect.right >=700:
                if d:
                    self.gridy += 1
            if self.rect.left <=50:
                if u: 
                    self.gridy -=1
            if self.rect.top <=120:
                if r:
                    self.gridx +=1
        self.x = (self.gridx-self.gridy)*tileWidthHalf
        self.y = (self.gridx+self.gridy)*tileHeightHalf

        self.rect = self.image.get_rect(center = (self.x, self.y))

    def render(self,screen):
        #ADD TO DATA DICTIONARY
        self.animationState()
        self.rect = self.image.get_rect(center = (self.x + 125, self.y + 195))
        self.move = True
        screen.blit(self.image, self.rect)

        if self.rect.left <= 50: 
            self.move = False
        if self.rect.right >= 700:
            self.move = False
        if self.rect.top <=120:
            self.move = False
            
#Game Function
def game(gameOn, scored, obstaclesList):    
    #CHANGE NAMES OF FIRST TWO LOCAL VARIABLES
    screen.fill('white')
    screen.blit(backgroundSurf, backgroundRect)
    pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(320,320,800,210))
    pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(700, 300, 100, 20))
    
    scored = displayScore()

    #Obstacle Movement

    obstaclesList = obstacleMovement(obstaclesList)

    mousePlayer.render(screen)

    mouseRect = mousePlayer.rect

    gameOn = collisions(mouseRect, obstacleRectList)

    inputs = pygame.key.get_pressed()

    #udlr -> Up, Down, Left and Right
    inputs_udlr = (inputs[K_UP],inputs[K_DOWN],inputs[K_LEFT],inputs[K_RIGHT])
    mousePlayer.update(inputs_udlr) #Update player with given udlr input

    if score >= 100:
        screen.fill('yellow')

    #print(score)
    return gameOn, scored, obstaclesList

#Obstacle Movement Function
def obstacleMovement(obstacleList):
    if obstacleList:
        for obstacleRect in obstacleList:
            obstacleRect.x -= 10
            obstacleRect.y -=4 

            if obstacleRect.width < pillowSurf.get_width() or obstacleRect.height < pillowSurf.get_height():
                screen.blit(ballSurf, obstacleRect)
            else:
                screen.blit(pillowSurf, obstacleRect)
    
        obstacleList = [obstacle for obstacle in obstacleList if obstacle.x > 200]

        return obstacleList
    else: 
        return []

#Collision Function
def collisions(player, obstacles):
    #ADD TO DICTIONARY
    if obstacles:
        for obstacleRect in obstacles:
            if player.colliderect(obstacleRect):
                obstacleRect.x = obstacleRect.width  
                obstacleRect.y = -obstacleRect.height 
                return False
    return True

#Score Function
def displayScore():
    #ADD TO DICTIONARY
    currentTime = (pygame.time.get_ticks() // 900) - startTime
    scoreSurf = font.render(f'Score: {currentTime}', False, 'black')
    scoreRect = scoreSurf.get_rect(center = (130, 75))
    screen.blit(scoreSurf, scoreRect)
    return currentTime

#Help Page Function
def helpInstructions():
    #ADD TO DICTIONARY
    screen.fill('white')
    help = font.render('USE UP, DOWN, LEFT AND ARROW KEYS', (False), ('black'))
    help1 = font.render('TO MOVE JERRY AWAY FROM THE OBSTACLES', (False), ('black'))
    helpRect =  help.get_rect(center = (400, 150))

    screen.blit(help, helpRect)
    screen.blit(help1, (130, 170))

    screen.blit(gameInstruction, gameInstructionRect)

#Home Page Function
def homePage():
    screen.fill('white')

    buttonSurf = pygame.Surface((150, 50))
    buttonRect = pygame.Rect(300, 400, 500, 500)
    buttonText = font.render('Help', True, ('black'))
    buttonTextRect = buttonText.get_rect(center = (buttonSurf.get_width()/2, buttonSurf.get_height()/2))

    if buttonRect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(buttonSurf, (128, 128, 128), (1, 1, 148, 48))
    else:
        pygame.draw.rect(buttonSurf, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(buttonSurf, (202, 202, 202), (1, 1, 148, 48))
        pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 1, 148, 1), 2)
        pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 48, 148, 10), 2)

    buttonSurf.blit(buttonText, buttonTextRect)
    screen.blit(buttonSurf, buttonRect)

    screen.blit(mouseAndCatSurf, mouseAndCatRect)
    screen.blit(gameMessage, gameMessageRect)
    screen.blit(gameInstruction, gameInstructionRect)

#Play Again Function
def playAgainPage():
    screen.fill('white')
    scoreMessage = font.render(f'Your score: {score}', False, ('black'))
    scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
    screen.blit(scoreMessage, scoreMessageRect)
    screen.blit(mouseAndCatSurf, mouseAndCatRect)

#End Page Function
def endPage():
    screen.fill('white')
    scoreMessage = font.render(f'JERRY CAN GET HIS CHEESE', False, ('black'))
    scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
    screen.blit(scoreMessage, scoreMessageRect)
    screen.blit(mouseAndCatSurf, mouseAndCatRect)

#Background
backgroundSurf = pygame.transform.scale(pygame.image.load('graphics/isometricRoom2.png'), (800, 510))
backgroundRect = backgroundSurf.get_rect(topleft = (50, 2))

#Main Character/Protagonist
mouseSurf = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
mousePlayer = Player(30,30)

#Obstacles/Antagonist
pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (100, 75))
pillowRect = pillowSurf.get_rect(center = (800, 487))
ballSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/ball.png'), (90, 74))
ballRect = ballSurf.get_rect(center = (800, 487))
obstacleRectList = []

#Game Messages: ADD TO DATA DICTIONARY
gameMessage = font.render('COMPLETE THE GAME FOR JERRY TO GET HIS CHEESE', (False), ('black'))
gameMessageRect = gameMessage.get_rect(center =(400, 50))


gameInstruction = font.render('PRESS SPACEBAR TO PLAY', False, 'black')
gameInstructionRect = gameInstruction.get_rect(center = (400, 360))

#Game Images
mouseAndCatSurf = pygame.transform.scale(pygame.image.load('graphics/menus/jerryAndTom.png'), (450, 215)).convert_alpha()
mouseAndCatRect = mouseAndCatSurf.get_rect(center = (400, 190))

#Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameActive:
            gameStart = True
            gameActive = True
            helpScreen = False
            startTime = (pygame.time.get_ticks() // 900)
            pillowRect.bottom = 487
            pillowRect.left = 800
            ballRect.bottom = 487
            ballRect.left = 800
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not gameActive:
                print('Going to Help Screen')
                helpScreen = True
        if event.type == obstacleTimer and gameActive:
            if randint(0,2):
                obstacleRectList.append(pillowSurf.get_rect(center = (randint(450, 900), randint (200, 487))))
            else:
                obstacleRectList.append(ballSurf.get_rect(center = (randint(450, 900), randint (200, 487))))

    if gameActive:
        gameActive, score, obstacleRectList = game(gameActive, score, obstacleRectList)

    if helpScreen:
        helpInstructions()

    if not gameActive and not helpScreen:
        if score == 0 and gameStart == False:
            homePage()
        if score > 0 and score <= 499:
            playAgainPage()
        if score > 0 and score == 500:
            endPage()

    pygame.display.flip() #Update everything
    
    clock.tick(60) #Steady fps