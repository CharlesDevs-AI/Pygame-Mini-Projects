import pygame
import random
import sys

pygame.init()

# -----------------------
# Screen
# -----------------------
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

clock = pygame.time.Clock()
FPS = 60

# -----------------------
# Colors
# -----------------------
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)

# -----------------------
# Road
# -----------------------
ROAD_LEFT = 100
ROAD_WIDTH = 300
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

# -----------------------
# Player
# -----------------------
player = pygame.Rect(220, 580, 60, 100)
player_speed = 7

# -----------------------
# Enemy
# -----------------------
enemy = pygame.Rect(
    random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 80),
    -120,
    60,
    100,
)

enemy_speed = 6

score = 0

line_y = 0

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    if player.left < ROAD_LEFT:
        player.left = ROAD_LEFT

    if player.right > ROAD_RIGHT:
        player.right = ROAD_RIGHT

    # Enemy Movement
    enemy.y += enemy_speed

    if enemy.top > HEIGHT:

        enemy.y = -120
        enemy.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 80)

        score += 1

        if score % 5 == 0:
            enemy_speed += 1

    # Collision
    if player.colliderect(enemy):
        break

    # Draw
    screen.fill((20, 120, 20))

    pygame.draw.rect(screen, BLACK, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    line_y += enemy_speed

    if line_y > 40:
        line_y = 0

    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (245, y + line_y, 10, 25))

    pygame.draw.rect(screen, BLUE, player)

    pygame.draw.rect(screen, RED, enemy)

    score_text = font.render(f"Score : {score}", True, YELLOW)

    screen.blit(score_text, (10, 10))

    pygame.display.update()

# -----------------------
# Game Over
# -----------------------
screen.fill(BLACK)

game = big_font.render("GAME OVER", True, RED)
score_text = font.render(f"Final Score : {score}", True, WHITE)
restart = font.render("Press R to Restart", True, GREEN)

screen.blit(game, (70, 220))
screen.blit(score_text, (145, 320))
screen.blit(restart, (120, 380))

pygame.display.update()

waiting = True

while waiting:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            waiting = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                pygame.quit()

                import os

                os.execl(sys.executable, sys.executable, *sys.argv)

            if event.key == pygame.K_ESCAPE:
                waiting = False

pygame.quit()