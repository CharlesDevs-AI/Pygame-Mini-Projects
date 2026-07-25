import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

WHITE=(255,255,255)
BLACK=(30,30,30)
BLUE=(70,140,255)
GREEN=(60,180,75)
RED=(220,70,70)
YELLOW=(240,220,0)

font=pygame.font.SysFont("arial",28)
big=pygame.font.SysFont("arial",42)

player=pygame.Rect(60,380,40,60)
spawn=(60,380)
vx=0
vy=0
SPEED=5
JUMP=-14
GRAVITY=0.75

platforms=[
    pygame.Rect(0,460,900,40),
    pygame.Rect(150,390,140,20),
    pygame.Rect(340,330,150,20),
    pygame.Rect(560,260,150,20),
    pygame.Rect(760,180,100,20)
]

coins=[
    pygame.Rect(200,355,20,20),
    pygame.Rect(410,295,20,20),
    pygame.Rect(620,225,20,20),
]

goal=pygame.Rect(820,130,40,50)

score=0
won=False

running=True
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_r:
                player.topleft=spawn
                vx=vy=0
                score=0
                won=False
                coins=[
                    pygame.Rect(200,355,20,20),
                    pygame.Rect(410,295,20,20),
                    pygame.Rect(620,225,20,20),
                ]

    keys=pygame.key.get_pressed()
    vx=0
    if keys[pygame.K_LEFT]:
        vx=-SPEED
    if keys[pygame.K_RIGHT]:
        vx=SPEED

    player.x+=vx

    vy+=GRAVITY
    player.y+=vy

    grounded=False
    for p in platforms:
        if player.colliderect(p) and vy>=0 and player.bottom-vy<=p.top+8:
            player.bottom=p.top
            vy=0
            grounded=True

    if keys[pygame.K_SPACE] and grounded:
        vy=JUMP

    if player.top>HEIGHT:
        player.topleft=spawn
        vy=0

    for c in coins[:]:
        if player.colliderect(c):
            coins.remove(c)
            score+=10

    if player.colliderect(goal) and not coins:
        won=True

    screen.fill((135,206,235))

    for p in platforms:
        pygame.draw.rect(screen,GREEN,p)

    for c in coins:
        pygame.draw.circle(screen,YELLOW,c.center,10)

    pygame.draw.rect(screen,RED,goal)
    pygame.draw.rect(screen,BLUE,player)

    screen.blit(font.render(f"Score: {score}",True,BLACK),(20,20))
    screen.blit(font.render(f"Coins Left: {len(coins)}",True,BLACK),(20,55))

    if won:
        t=big.render("YOU WIN! Press R",True,BLACK)
        screen.blit(t,(260,30))

    pygame.display.flip()

pygame.quit()
sys.exit()
