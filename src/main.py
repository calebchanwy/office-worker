import pygame
import os
import random
import time
import sys
import mainMenu
pygame.font.init()
pygame.init()

def writefile(name,score):
    f = open('winners.txt','a+')
    f.write("{},{}\n".format(name,score))
    f.close()

class Timeclock:
    def __init__(self):
        self.t = 0

    def delay(self,dt,time):
        #creating a class to allow us to observe a delay
        self.t+=dt
        if self.t>=time:
            self.t = 0
            return True
        else:
            return False

#constants
WHITE = (255,255,255)
PINK =  (255,203,208)
BLACK = (0,0,0)
RED = (255,0,0)

BORDERHEIGHT = 50
COFFEEWIDTH, COFFEEHEIGHT = 30, 30
COFFEESTATIONWIDTH, COFFEESTATIONHEIGHT = 100,180
BOSSWIDTH,BOSSHEIGHT = 50,90
CHARACTERWIDTH,CHARACTERHEIGHT = 50,70
BRIEFCASEWIDTH, BRIEFCASEHEIGHT = 30,30
DESKWIDTH, DESKHEIGHT = 140,140
DESKX, DESKY = 800,400
vel = 5
WIDTH, HEIGHT = 1000,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Office Worker")
vel = 5
bossvel = 1

#fonts
def fontInit(fontSize):
    return pygame.font.SysFont('bahnschrift',fontSize)
scorefont = fontInit(30)
mainMenuFont = fontInit(80)
buttonsFont = fontInit(50)

#user events
COLLECTBRIEF = pygame.USEREVENT+0
CREATEBRIEF = pygame.USEREVENT+1
pygame.time.set_timer(CREATEBRIEF, 2000)
DROPBRIEF = pygame.USEREVENT+2
COFFEEDELAY = pygame.USEREVENT+3
COFFEE = pygame.USEREVENT+4

#image loading
bossImg = pygame.image.load(os.path.join('assets','boss.png'))
bossImg = pygame.transform.scale(bossImg,(BOSSWIDTH,BOSSHEIGHT))
deskImg = pygame.image.load(os.path.join('assets','desk.png'))
deskImg = pygame.transform.scale(deskImg,(DESKWIDTH,DESKHEIGHT))
briefcaseImg = pygame.image.load(os.path.join('assets',"briefcase.png"))
briefcaseImg = pygame.transform.scale(briefcaseImg,(BRIEFCASEWIDTH,BRIEFCASEHEIGHT))
workerImage = pygame.image.load(os.path.join('assets','worker.png'))
workerImage = pygame.transform.scale(workerImage,(CHARACTERWIDTH,CHARACTERHEIGHT))
coffeeStationimg = pygame.image.load(os.path.join('assets','coffeeStation.png'))
coffeeStationimg = pygame.transform.scale(coffeeStationimg,(COFFEESTATIONWIDTH,COFFEESTATIONHEIGHT))
coffeeImg = pygame.image.load((os.path.join('assets','coffee.png')))
coffeeImg = pygame.transform.scale(coffeeImg,(COFFEEWIDTH,COFFEEHEIGHT))

class InputBox:
    def __init__(self,x,y,w,h,text = ''):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = PINK
        self.text = text
        self.txt_surface = scorefont.render(text,True,self.color)
    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.text
                
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = scorefont.render(self.text,True,BLACK)

    def draw(self,WIN):
        pygame.draw.rect(WIN,self.color,(self.rect.x,self.rect.y,self.rect.w,self.rect.h))
        WIN.blit(self.txt_surface,(self.rect.x+5,self.rect.y+5))




def handleworker(officeWorker,briefcases,desk,holdingBriefcases,deskbriefcases,coffeestation):
    for briefcase in briefcases:
        #if office worker collides with a free briefcase
        if officeWorker.colliderect(briefcase) and len(holdingBriefcases)!=1:
            holdingBriefcases.append(briefcase)
            #adds event COLLECTBRIEF to queue
            pygame.event.post(pygame.event.Event(COLLECTBRIEF))
            briefcases.remove(briefcase)    
    #if the office worker collides with desk and is carrying one briefcase
    if officeWorker.colliderect(desk) and len(holdingBriefcases)==1:
        #adds event DROPBRIEF to queue and gets boss to collect briefcase
        pygame.event.post(pygame.event.Event(DROPBRIEF))
        deskbriefcases.append(holdingBriefcases.pop())
    if officeWorker.colliderect(coffeestation):
        pygame.event.post(pygame.event.Event(COFFEE))

def handleBoss(boss,desk,deskbriefcases,bossbriefcases):
    if boss.x <= desk.x+60 and len(deskbriefcases)>=1:
        briefcase = deskbriefcases.pop()
        bossbriefcases.append(briefcase)

    if boss.x>=WIDTH and len(bossbriefcases)==1:
        bossbriefcases.pop()
        bosscollect = False

def drawWindow(officeWorker,briefcases,score,desk,holdingBriefcases,deskbriefcases,coffeeStation,coffee,boss,bossbriefcases):
    WIN.fill((150,200,150))
    WIN.blit(deskImg,(desk.x,desk.y))
    WIN.blit(coffeeStationimg,(coffeeStation.x,coffeeStation.y))
    #using enums to work out how many briefcases have already been drawn
    for index,briefcase in enumerate(deskbriefcases):
        WIN.blit(briefcaseImg,(desk.x+80,desk.y+40-index*(15)))
    WIN.blit(workerImage,(officeWorker.x,officeWorker.y))
    #off placing the briefcase to be at the worker's hand
    for briefcase in holdingBriefcases:
        WIN.blit(briefcaseImg,(officeWorker.x+25,officeWorker.y+35))
    for briefcase in briefcases:
        WIN.blit(briefcaseImg,(briefcase.x,briefcase.y))
    WIN.blit(bossImg,(boss.x,boss.y))
    for briefcase in bossbriefcases:
        WIN.blit(briefcaseImg,(boss.x-10,boss.y+40))
    if coffee == True:
        WIN.blit(coffeeImg,(officeWorker.x,officeWorker.y+30))

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

def gameEnd(score):
    WIN.fill(WHITE)
    drawText("GAME ENDED",mainMenuFont,BLACK,WIN,WIDTH//2,100,True,True)
    drawText("You Scored: {}".format(score),scorefont,BLACK,WIN,WIDTH//2,250,True,False)
    drawText("Enter your name:",scorefont,BLACK,WIN,WIDTH//2,300,True,False)
    drawText("Press Escape to continue to menu...",scorefont,BLACK,WIN,WIDTH//2,500,True,False)
    inputName = InputBox(100,370,800,50)
    while True:
        for event in pygame.event.get():
            WIN.fill(WHITE)
            drawText("GAME ENDED",mainMenuFont,BLACK,WIN,WIDTH//2,100,True,True)
            drawText("You Scored: {}".format(score),scorefont,BLACK,WIN,WIDTH//2,250,True,False)
            drawText("Enter your name:",scorefont,BLACK,WIN,WIDTH//2,300,True,False)
            drawText("Press Escape to continue to menu...",scorefont,BLACK,WIN,WIDTH//2,500,True,False)
            if event.type == pygame.KEYDOWN:
                if event.key  == pygame.K_ESCAPE:
                    mainMenu.mainMenu()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            name = inputName.handleEvent(event)
            inputName.draw(WIN)
            if name:
                writefile(name,score)
                mainMenu.mainMenu()
       
        pygame.display.update()
    

def drawBorder(score,health):
    #drawing white border
    pygame.draw.rect(WIN,WHITE,(0,0,WIDTH,BORDERHEIGHT))
    #drawing the health bar with a black outline
    pygame.draw.rect(WIN,BLACK,(295,6,310,37))
    pygame.draw.rect(WIN,RED,(300,12,health*3,25))
    #drawing score
    scoreText = scorefont.render("Score : "+str(score),1,BLACK)
    WIN.blit(scoreText,(5,5))

def workermotion(officeWorker,keysPressed):
    #wasd controls to move with velocity
    if keysPressed[pygame.K_w] and officeWorker.y-vel>0+BORDERHEIGHT:
        officeWorker.y-=vel
    if keysPressed[pygame.K_s] and officeWorker.y+vel+CHARACTERHEIGHT<HEIGHT:
        officeWorker.y+=vel
    if keysPressed[pygame.K_a] and officeWorker.x-vel>0:
        officeWorker.x-=vel
    if keysPressed[pygame.K_d] and officeWorker.x+vel+CHARACTERWIDTH<WIDTH:
        officeWorker.x+=vel
        
def bossMotion(boss,desk,bossbriefcases,deskbriefcases):
    if len(deskbriefcases)>=1 and boss.x>desk.x+60 and len(bossbriefcases)==0:
        boss.x-=bossvel
    elif len(bossbriefcases)==1:
        boss.x+=bossvel

def main():
    #initalising empty lists to hold the briefcases data
    briefcases = []
    holdingBriefcases = []
    deskbriefcases = []
    bossbriefcases = []
    officeWorker = pygame.Rect(425,170,CHARACTERHEIGHT,CHARACTERHEIGHT)
    desk = pygame.Rect(DESKX,DESKY,DESKWIDTH,DESKHEIGHT)
    coffeeStation = pygame.Rect(100,150,COFFEESTATIONWIDTH,COFFEESTATIONHEIGHT)
    boss = pygame.Rect(WIDTH,desk.y+40,BOSSWIDTH,BOSSHEIGHT)
    run = True
    #timers to allow observation of time for delays/set intervals
    clock = pygame.time.Clock()
    healthTimer = Timeclock()
    score = 0
    health = 100
    startHealth = 0
    coffee = False
    healthdegrade = True
    bosscollect = False
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            #if application is closed, allows game exit while loop
            if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
            if event.type == CREATEBRIEF:
                #placing briefcase at random times, at random locations
                briefcase = pygame.Rect(random.randint(0,WIDTH-BRIEFCASEWIDTH),random.randint(BORDERHEIGHT,HEIGHT-BRIEFCASEHEIGHT),BRIEFCASEWIDTH,BRIEFCASEHEIGHT)
                briefcases.append(briefcase)
                #preventing spawning of a briefcase which collides with the desk, worker or coffee station
                if briefcase.colliderect(coffeeStation) or briefcase.colliderect(desk) or briefcase.colliderect(officeWorker) or briefcase.colliderect(boss):
                    briefcases.pop()
                pygame.time.set_timer(CREATEBRIEF, random.randint(2000,3000))
            if event.type == DROPBRIEF:
                score+=1
                health-=2
            if event.type == COLLECTBRIEF:
                health-=2
            if event.type == COFFEEDELAY:
                healthdegrade = True
                coffee = False
                dt = clock.get_time()
                if healthTimer.delay(dt,2500):
                    startHealth = 0
            if  event.type== COFFEE and event.type !=COFFEEDELAY:
                if health >= 100:
                    coffee = False
                    healthdegrade = True
                    health = 100
                elif startHealth<20:
                    healthdegrade = False
                    coffee = True
                    health +=1
                    startHealth+=1
                elif startHealth >=20:
                    healthdegrade = True
                    coffee = False
                    pygame.event.post(pygame.event.Event(COFFEEDELAY))
            else:
                healthdegrade = True
                coffee = False
            if health<=0:
                gameEnd(score)

        if healthdegrade == True:
            health-=0.025
        handleworker(officeWorker,briefcases,desk,holdingBriefcases,deskbriefcases,coffeeStation)
        handleBoss(boss,desk,deskbriefcases,bossbriefcases)
        keysPressed = pygame.key.get_pressed()
        workermotion(officeWorker,keysPressed)
        bossMotion(boss,desk,bossbriefcases,deskbriefcases)
        drawWindow(officeWorker,briefcases,score,desk,holdingBriefcases,deskbriefcases,coffeeStation,coffee,boss,bossbriefcases)
        drawBorder(score,health)
        pygame.display.update()

if __name__ == "__main__": 
    mainMenu.mainMenu()