import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
ROWS, COLS = 4, 4
CARD_SIZE = 100
PADDING = 20
TOP = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 28)
BIG = pygame.font.SysFont("arial", 48)

WHITE=(255,255,255)
BLACK=(30,30,30)
BLUE=(70,120,255)
GREEN=(60,180,75)
GRAY=(180,180,180)

def new_game():
    nums=list(range(1,9))*2
    random.shuffle(nums)
    cards=[]
    sx=(WIDTH-(COLS*CARD_SIZE+(COLS-1)*PADDING))//2
    sy=TOP
    i=0
    for r in range(ROWS):
        for c in range(COLS):
            x=sx+c*(CARD_SIZE+PADDING)
            y=sy+r*(CARD_SIZE+PADDING)
            cards.append({
                "rect":pygame.Rect(x,y,CARD_SIZE,CARD_SIZE),
                "value":nums[i],
                "revealed":False,
                "matched":False
            })
            i+=1
    return cards

cards=new_game()
first=None
second=None
waiting=False
wait_start=0
moves=0
matches=0

running=True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    if waiting and pygame.time.get_ticks()-wait_start>800:
        first["revealed"]=False
        second["revealed"]=False
        first=None
        second=None
        waiting=False

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_r:
                cards=new_game()
                first=second=None
                waiting=False
                moves=0
                matches=0
        elif e.type==pygame.MOUSEBUTTONDOWN and not waiting and matches<8:
            pos=e.pos
            for card in cards:
                if card["rect"].collidepoint(pos):
                    if card["matched"] or card["revealed"]:
                        break
                    card["revealed"]=True
                    if first is None:
                        first=card
                    else:
                        second=card
                        moves+=1
                        if first["value"]==second["value"]:
                            first["matched"]=True
                            second["matched"]=True
                            matches+=1
                            first=None
                            second=None
                        else:
                            waiting=True
                            wait_start=pygame.time.get_ticks()
                    break

    screen.blit(FONT.render(f"Moves: {moves}",True,WHITE),(20,20))
    screen.blit(FONT.render(f"Matches: {matches}/8",True,WHITE),(600,20))

    for card in cards:
        if card["revealed"] or card["matched"]:
            pygame.draw.rect(screen,GREEN,card["rect"],border_radius=8)
            t=FONT.render(str(card["value"]),True,WHITE)
            screen.blit(t,t.get_rect(center=card["rect"].center))
        else:
            pygame.draw.rect(screen,BLUE,card["rect"],border_radius=8)
            pygame.draw.rect(screen,WHITE,card["rect"],2,border_radius=8)
            q=FONT.render("?",True,WHITE)
            screen.blit(q,q.get_rect(center=card["rect"].center))

    if matches==8:
        win=BIG.render("YOU WIN!",True,GREEN)
        msg=FONT.render("Press R to Play Again",True,WHITE)
        screen.blit(win,win.get_rect(center=(WIDTH//2,35)))
        screen.blit(msg,msg.get_rect(center=(WIDTH//2,570)))

    pygame.display.flip()

pygame.quit()
sys.exit()

