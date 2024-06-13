# *** File: jerryAvoidTheObstacles-v1.py***

# *** Author: Ysbelle Orozco ***

# *** Date: 28th of May 2024 ***

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
gameActive = True  
startTime = 0

def displayScore():
    currentTime = (pygame.time.get_ticks() // 1000) - startTime
    scoreSurf = font.render(f'Score: {currentTime}', False, (64, 64, 64))
    scoreRect = scoreSurf.get_rect(center = (430, 50))
    screen.blit(scoreSurf, scoreRect)

backgroundSurf = pygame.image.load('graphics/bedroom.png').convert()

mouseSurf = pygame.transform.scale(pygame.image.load('graphics/Player/1.png'), (100, 75)).convert_alpha()
mouseRect = mouseSurf.get_rect(midbottom = (360, 450))

loadCatSurf = pygame.transform.scale(pygame.image.load('graphics/Player/4.png'), (200, 150)).convert_alpha()
flipCatSurf = pygame.transform.flip(loadCatSurf, False, True)
catSurf = pygame. transform.rotate(flipCatSurf, 180)
catRect = catSurf.get_rect(bottomright = (150, 450))

#scoreSurf = scoreFont.render('Score', False, 'black')

pillowSurf = pygame.transform.scale(pygame.image.load('graphics/obstacles/pillow.png'), (75, 50))                                                                                                                                           
pillowRect = pillowSurf.get_rect(bottomright = (900, 450))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and mouseRect.bottom >= 300:
                    mouseGravity = -23
        else:      
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                pillowRect.left = 980
                startTime = (pygame.time.get_ticks() // 1000)

    if gameActive: 
        screen.blit(backgroundSurf, (0, 0))
        displayScore()

        #mouse
        mouseGravity +=1
        mouseRect.y += mouseGravity
        if mouseRect.bottom >= 450:
            mouseRect.bottom = 450
        screen.blit(mouseSurf, mouseRect)

        screen.blit(catSurf, catRect)

        pillowRect.x -= 6
        if pillowRect.right <= 0:
            pillowRect.left = 980
        screen.blit(pillowSurf, pillowRect)

        #collison

        if pillowRect.colliderect(mouseRect):
            gameActive = False
    
    else:
        screen.fill('yellow')

    pygame.display.update()
    clock.tick(60)