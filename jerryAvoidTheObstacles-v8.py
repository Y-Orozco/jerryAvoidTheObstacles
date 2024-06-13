# *** File: jerryAvoidTheObstacles-v8.py ***

# *** Author: Ysbelle Orozco ***

# *** Date: 11th of June 2024 ***

import pygame
from pygame.locals import *
from random import randint, choice

pygame.init()

screenWidth = 800
screenHeight = 487
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
gameStart = False #Start of the actual program running
gameActive = False #Game function displaying or not
startTime = 0
score = 0
helpScreen = False
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 1200)
mouseLives = 0
obstacleGroup = pygame.sprite.Group()

#Sound
bgMusic = pygame.mixer.Sound('audio/maltShopBop.mp3') #Background Music
bgMusic.set_volume(0.7) #Lower bgMusic volume
bgMusic.play(loops = -1)
collidingSound = pygame.mixer.Sound('audio/colliding.mp3')

#For Isometric Movement
tileWidth  = 16 
tileWidthHalf = tileWidth/2
tileHeight = 6
tileHeightHalf = tileHeight/2

pygame.display.set_caption('Jerry, Avoid The Obstacles!') #Name of Window

#Main Character Class
class Player(pygame.sprite.Sprite):
    def __init__(self,gridx,gridy):
        #Initialising variables:

        self.gridx = gridx
        self.gridy = gridy
        
        #Mouse images for animating frame
        self.mouseSurf1 = pygame.transform.scale(pygame.image.load('graphics/Player/mouse1.png'), (100, 75)).convert_alpha()
        self.mouseSurf2 = pygame.transform.scale(pygame.image.load('graphics/Player/mouse2.png'), (100, 75)).convert_alpha()
        self.mouseSurf3 = pygame.transform.scale(pygame.image.load('graphics/Player/mouse3.png'), (100, 75)).convert_alpha()
        self.mouseSurf4 = pygame.transform.scale(pygame.image.load('graphics/Player/mouse4.png'), (100, 75)).convert_alpha()

        #List for animating frame mouse images
        self.mouseWalk = [self.mouseSurf1, self.mouseSurf2, self.mouseSurf3, self.mouseSurf4]

        self.mouseIndex = 0
        self.image = self.mouseWalk[self.mouseIndex]
        self.x = (self.gridx-self.gridy)*tileWidthHalf
        self.y = (self.gridx+self.gridy)*tileHeightHalf

    def animationState(self):
        #Animation Frame
        self.mouseIndex += 0.1 #Increments the mouseIndex
        if self.mouseIndex >= len(self.mouseWalk): 
            self.mouseIndex = 0 #Goes back to the first mouseIndex
        self.image = self.mouseWalk[int(self.mouseIndex)] #Displays mouse according to the MouseIndex

    def update(self, udlr):
        u,d,l,r = udlr #Extract key info
        if self.move:
            if u:
                self.gridy -= 1 #Moves diagonally left bottom from right top
            elif d:
                self.gridy += 1 #Moves diagonally right top from left bottom
            elif l:
                self.gridx -= 1 #Moves diagonally left top from right bottom
            elif r:
                self.gridx += 1 #Moves diagonally bottom right from top left
        else:
            self.move=False
            if self.rect.right >=700: #Right Boundary
                if d:
                    self.gridy += 1 #Allowed movement is down
            if self.rect.left <=50: #Left Boundary
                if u: 
                    self.gridy -=1 #Allowed movement is up
            if self.rect.top <=120: #Top Boundary
                if r:
                    self.gridx +=1 #Allowed Movement is right

        self.x = (self.gridx-self.gridy)*tileWidthHalf
        self.y = (self.gridx+self.gridy)*tileHeightHalf
        #Takes the grid coordinate and translates it to pixel coordinates

        self.rect = self.image.get_rect(center = (self.x, self.y)) #Initialise rect

    def render(self,screen):
        self.animationState() #Calls animationState() function
        self.rect = self.image.get_rect(center = (self.x + 125, self.y + 195))
        self.move = True #Initialise Flag
        screen.blit(self.image, self.rect) #Display mouse

        #Restricting the character's movement by preventing the hitbox from going off-screen
        if self.rect.left <= 50: 
            self.move = False #Flag
        if self.rect.right >= 700:
            self.move = False
        if self.rect.top <=120:
            self.move = False
            
#Antagonist Obstacle Sprite Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'ball':
            #If ball is chosen, display ball
            ballSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/ball.png'), (90, 74)).convert_alpha()
            self.image = ballSurf
        else:
            #If ball is not chosen, display pillow
            pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (100, 75)).convert_alpha()
            self.image = pillowSurf
        
        self.rect = self.image.get_rect(center = (randint(450, 850), randint (250, 487))) #Initialise rect

    def update(self):
        #Move obstacles diagonally from right bottom to left top
        self.rect.x -= 10
        self.rect.y -=4
        if score >= 39:
            #Faster speed once score reaches specific score
            self.rect.x -= 11
            self.rect.y -=4.5
        self.destroy() 

    def destroy(self):
        if self.rect.x < 200: #Obstacle destroys after reaching a certain point
            self.kill()

#Game Function
def game(gameOn, userScore, obstaclesList, lives, sound):    
    screen.fill('white')
    screen.blit(backgroundSurf, backgroundRect) #Isometric room

    #Rectangle covers the gaps between the background and screen
    pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(320,320,800,210))
    pygame.draw.rect(screen, (237, 217, 147), pygame.Rect(700, 300, 100, 20))
    
    userScore = displayScore() #Displayed score function

    #Obstacle Movement
    obstacleGroup.draw(screen)
    obstacleGroup.update()

    mousePlayer.render(screen) #Mouse display

    gameOn = collisionSprite() #Collision detection

    displayLives(lives) #Amount of Lives function

    if not gameOn:
        #Collision
        lives += 1 #Lives incremented
        sound.set_volume(0.5) #Lowers sound volume
        sound.play() #Sound of colliding
        gameOn = True
        if lives == 3:
            gameOn = False #End game after no lives

    inputs = pygame.key.get_pressed() #Get input

    #udlr -> Up, Down, Left and Right
    inputs_udlr = (inputs[K_UP],inputs[K_DOWN],inputs[K_LEFT],inputs[K_RIGHT])
    mousePlayer.update(inputs_udlr) #Update player with given udlr input

    if userScore >= 50: 
        endPage() #End game when user's score is 50

    return gameOn, userScore, obstaclesList, lives, sound

def displayLives(lives):
    #Displays the hearts that are lives on the screen
    if lives == 0:
        screen.blit(heartSurf, heartRect1)
        screen.blit(heartSurf, heartRect2)
        screen.blit(heartSurf, heartRect3)
    if lives == 1:
        screen.blit(heartSurf, heartRect2)
        screen.blit(heartSurf, heartRect3)
    if lives == 2:
        screen.blit(heartSurf, heartRect3)

#Collision Sprite Function
def collisionSprite():
    if pygame.sprite.spritecollide(mousePlayer, obstacleGroup, False):
        obstacleGroup.empty() #Clears obstacleGroup
        return False
    else:
        return True

#Score Function
def displayScore():
    currentTime = (pygame.time.get_ticks() // 500) - startTime #Initialises score and speed
    scoreSurf = font.render(f'Score: {currentTime}', False, 'black') 
    scoreRect = scoreSurf.get_rect(center = (130, 75))
    screen.blit(scoreSurf, scoreRect) #Displays score
    return currentTime

#Help Page Function
def helpInstructions():
    screen.fill('white')
    screen.blit(helpGraphicSurf, (0,0)) #Displays help graphic

#Home Page Function
def homePage():
    screen.fill('white')

    #Displays Button
    buttonSurf = pygame.Surface((150, 50))
    buttonRect = pygame.Rect(300, 400, 500, 500)
    buttonText = font.render('Help', True, ('black'))
    buttonTextRect = buttonText.get_rect(center = (buttonSurf.get_width()/2, buttonSurf.get_height()/2))

    if buttonRect.collidepoint(pygame.mouse.get_pos()): #Turns button darker when mouse hovers over it
        pygame.draw.rect(buttonSurf, (128, 128, 128), (1, 1, 148, 48))
    else:
        #Normal state of button
        pygame.draw.rect(buttonSurf, (0, 0, 0), (0, 0, 150, 50))
        pygame.draw.rect(buttonSurf, (202, 202, 202), (1, 1, 148, 48))
        pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 1, 148, 1), 2)
        pygame.draw.rect(buttonSurf, (0, 0, 0), (1, 48, 148, 10), 2)

    #Displays Button Text
    buttonSurf.blit(buttonText, buttonTextRect)
    screen.blit(buttonSurf, buttonRect)

    #Display graphic and messages
    screen.blit(happyMouseSurf, happyMouseRect)
    screen.blit(gameMessage, gameMessageRect) #Game objective
    screen.blit(gameInstruction, gameInstructionRect) #Tells users how to play the game

#Play Again Function
def playAgainPage():
    screen.fill('white') #Clears screen
    scoreMessage = font.render(f'Your score: {score}', False, ('black'))
    scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
    
    screen.blit(scoreMessage, scoreMessageRect)
    screen.blit(sadMouseSurf, sadMouseRect)
    screen.blit(gameInstruction, gameInstructionRect) #Ask user's to play again

#End Page Function
def endPage():
    screen.fill('white')
    scoreMessage = font.render(f'CONGRATS! YOU WON', False, ('black')) #End game congratiulations
    scoreMessageRect = scoreMessage.get_rect(center = (400, 50))
    screen.blit(scoreMessage, scoreMessageRect)
    screen.blit(happyMouseSurf, happyMouseRect)

#Background
backgroundSurf = pygame.transform.scale(pygame.image.load('graphics/isometricRoom2.png'), (800, 510))
backgroundRect = backgroundSurf.get_rect(topleft = (50, 2))

#Main Character/Protagonist
mouseSurf = pygame.transform.scale(pygame.image.load('graphics/Player/mouse1.png'), (100, 75)).convert_alpha()
mousePlayer = Player(30,30)

#Obstacles/Antagonist
pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (100, 75)).convert_alpha()
pillowRect = pillowSurf.get_rect(center = (800, 487))
ballSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/ball.png'), (90, 74)).convert_alpha()
ballRect = ballSurf.get_rect(center = (800, 487))
obstacleRectList = []

#Game Messages: 
gameMessage = font.render('HELP JERRY AVOID THE OBSTACLES', (False), ('black'))
gameMessageRect = gameMessage.get_rect(center =(400, 50))

gameInstruction = font.render('PRESS SPACEBAR TO PLAY', False, 'black')
gameInstructionRect = gameInstruction.get_rect(center = (400, 360))

#Game Images
happyMouseSurf = pygame.transform.scale(pygame.image.load('graphics/menus/happyMouse.png'), (380, 215)).convert_alpha()
happyMouseRect = happyMouseSurf.get_rect(center = (400, 190)) 

sadMouseSurf = pygame.transform.scale(pygame.image.load('graphics/menus/sadMouse.png'), (280, 215)).convert_alpha()
sadMouseRect = sadMouseSurf.get_rect(center = (400, 190)) 

#Heart Images for Lives
heartSurf = pygame.transform.scale(pygame.image.load('graphics/heart.png'), (30, 28)).convert_alpha()
heartRect1 = heartSurf.get_rect(center = (700, 455))
heartRect2 = heartSurf.get_rect(center = (735, 455))
heartRect3 = heartSurf.get_rect(center = (770, 455))

helpGraphicSurf = pygame.transform.scale(pygame.image.load('graphics/menus/helpImg.png'), (screenWidth, screenHeight))

#Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameActive:
            gameStart = True #Start of program
            gameActive = True #Game function displaying
            helpScreen = False #Help function not displaying 
            startTime = (pygame.time.get_ticks() // 500)
            pillowRect.bottom = 487 #Start position pillow
            pillowRect.left = 800 
            ballRect.bottom = 487 #Start position ball
            ballRect.left = 800 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not gameActive:
                print('Going to Help Screen')
                helpScreen = True #Goes to help function
        if event.type == obstacleTimer and gameActive:
            if score <= 24:
                #Pillow is the only obstacle until it reaches a certain score
                obstacleGroup.add(Obstacle('pillow'))
            else:
                #Chooses between ball or pillow as an obstacle
                obstacleGroup.add(Obstacle(choice(['ball', 'pillow'])))

    if gameActive:
        #Game function called
        gameActive, score, obstacleRectList, mouseLives, collidingSound = game(gameActive, score, obstacleRectList, mouseLives, collidingSound)

    if helpScreen:
        #Help functino called
        helpInstructions()

    if not gameActive and not helpScreen:
        if score == 0 and gameStart == False:
            #Beginning page
            homePage()
        if score > 0 and score <= 49:
            mouseLives = 0 #Sets lives back 
            playAgainPage() #Allows the user to play again
        if score > 0 and score >= 50:
            endPage()

    pygame.display.flip() #Update everything
    
    clock.tick(60) #Steady fps