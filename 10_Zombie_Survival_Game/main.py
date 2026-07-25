import pygame, random, sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()

WHITE=(255,255,255)
BLACK=(25,25,25)
GREEN=(60,180,75)
RED=(220,60,60)
BLUE=(70,140,255)

font=pygame.font.SysFont("arial",28)
big=pygame.font.SysFont("arial",42)

player=pygame.Rect(WIDTH//2-20, HEIGHT//2-20, 40,40)
speed=5

zombies=[]
spawn_timer=0
score=0
game_over=False

while True:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type==pygame.KEYDOWN and e.key==pygame.K_r and game_over:
            player.x,player.y=WIDTH//2-20,HEIGHT//2-20
            zombies.clear()
            score=0
            spawn_timer=0
            game_over=False

    if not game_over:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x-=speed
        if keys[pygame.K_RIGHT]: player.x+=speed
        if keys[pygame.K_UP]: player.y-=speed
        if keys[pygame.K_DOWN]: player.y+=speed

        player.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))

        spawn_timer+=1
        if spawn_timer>=45:
            spawn_timer=0
            side=random.randint(0,3)
            if side==0:
                x,y=random.randint(0,WIDTH),-30
            elif side==1:
                x,y=random.randint(0,WIDTH),HEIGHT+30
            elif side==2:
                x,y=-30,random.randint(0,HEIGHT)
            else:
                x,y=WIDTH+30,random.randint(0,HEIGHT)
            zombies.append(pygame.Rect(x,y,30,30))

        for z in zombies:
            dx=player.centerx-z.centerx
            dy=player.centery-z.centery
            d=max((dx*dx+dy*dy)**0.5,1)
            z.x+=int(dx/d*2)
            z.y+=int(dy/d*2)
            if z.colliderect(player):
                game_over=True

        score+=1

    screen.fill(BLACK)
    pygame.draw.rect(screen,BLUE,player)

    for z in zombies:
        pygame.draw.rect(screen,GREEN,z)

    screen.blit(font.render(f"Score: {score}",True,WHITE),(15,15))

    if game_over:
        t=big.render("GAME OVER",True,RED)
        r=font.render("Press R to Restart",True,WHITE)
        screen.blit(t,t.get_rect(center=(WIDTH//2,250)))
        screen.blit(r,r.get_rect(center=(WIDTH//2,310)))

    pygame.display.flip()
