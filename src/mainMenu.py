import pygame
import os
import random
import time
import sys
import main
pygame.font.init()
pygame.init()

WHITE = (255,255,255)
PINK =  (255,203,208)
BLACK = (0,0,0)

#fonts
def fontInit(fontSize):
    return pygame.font.SysFont('bahnschrift',fontSize)
subtitleFont = fontInit(20)
mainMenuFont = fontInit(80)
buttonsFont = fontInit(50)
creditsFont = fontInit(20)

WIDTH, HEIGHT = 1000,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Office Worker")

arrowImg = pygame.image.load((os.path.join('assets','arrow.png')))
arrowImg = pygame.transform.scale(arrowImg,(50,50))

def readfile(filename):
    f = open(filename,"r")
    contents = f.read()
    f.close()
    return contents

def drawText(text,font,colour,WIN,x,y,centered,button):
    textobj = font.render(text,1,colour)
    textRect = textobj.get_rect()
    if centered == True:
        if button == True:
            pygame.draw.rect(WIN,PINK,(x-textRect.centerx-5,y-5,textRect.width+10,textRect.height+10))
            buttonrect = pygame.Rect(x-textRect.centerx-5,y-5,textRect.width+10,textRect.height+10)
            WIN.blit(textobj,(x-textRect.centerx,y))
            return buttonrect
        else:
            WIN.blit(textobj,(x-textRect.centerx,y))
    else:
        WIN.blit(textobj,(x,y))

def creditsFunc():
    WIN.fill(WHITE)
    creditText = readfile("credits.txt")
    creditText = creditText.split("\n")
    for i in range (len(creditText)):
        drawText(creditText[i],creditsFont,BLACK,WIN,50,50+i*50,False,False)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def leaderboard():
    myDict = {}
    winners = readfile((os.path.join('src','winners.txt')))
    winners = winners.split("\n")
    winners.remove("")
    for winner in winners:
        winner = winner.split(",")
        myDict[winner[0]] = int(winner[1])
    myDict = dict(sorted(myDict.items(), key=lambda item: item[1],reverse = True))
    drawText("Top 5 Players:",subtitleFont,BLACK,WIN,50,175,False,True)
    for i in range (5):
        name = list(myDict)[i]
        score = myDict[name]
        temp = "{}, {}".format(name, str(score))
        drawText(temp,subtitleFont,BLACK,WIN,50,225+i*50,False,True)
    

def mainMenu():
    WIN.fill(WHITE)
    drawText("Main Menu",mainMenuFont,BLACK,WIN,WIDTH//2,30,True,False)
    button1 = drawText("PLAY GAME",buttonsFont,BLACK,WIN,WIDTH//2,200,True,True)
    button2 = drawText("CREDITS",buttonsFont,BLACK,WIN,WIDTH//2,300,True,True)
    button3 = drawText("QUIT",buttonsFont,BLACK,WIN,WIDTH//2,400,True,True)
    buttons = [button1,button2,button3]
    drawText("Use w and s or the arrow keys to move up and down...",subtitleFont,BLACK,WIN,WIDTH//2,550,True,False)
    currbutton = 0
    arrow = pygame.Rect(button1.x-70,button1.y,50,50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    currbutton-=1
                    if currbutton<0:
                        currbutton+=1
                    arrow.y = buttons[currbutton].y
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    currbutton +=1
                    if currbutton>2:
                        currbutton-=1
                    arrow.y = buttons[currbutton].y
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if buttons[currbutton] == button3:
                        pygame.quit()
                        sys.exit()
                    if buttons[currbutton] == button1:
                        main.main()
                    if buttons[currbutton] == button2:
                        creditsFunc()
        
        #updating display
        WIN.fill(WHITE)
        drawText("Office Worker",mainMenuFont,BLACK,WIN,WIDTH//2,30,True,False)
        button1 = drawText("PLAY GAME",buttonsFont,BLACK,WIN,WIDTH//2,200,True,True)
        button2 = drawText("CREDITS",buttonsFont,BLACK,WIN,WIDTH//2,300,True,True)
        button3 = drawText("QUIT",buttonsFont,BLACK,WIN,WIDTH//2,400,True,True)
        drawText("Use w and s or the arrow keys to move up and down...",subtitleFont,BLACK,WIN,WIDTH//2,550,True,False)
        WIN.blit(arrowImg,(arrow.x,arrow.y))
        leaderboard()
        pygame.display.update()


mainMenu()
