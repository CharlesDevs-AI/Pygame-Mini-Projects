import pygame
import random
import sys

pygame.init()

# ==========================================
# Screen Settings
# ==========================================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
FPS = 60

# ==========================================
# Colors
# ==========================================
BLACK = (20, 20, 30)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
BLUE = (80, 180, 255)

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

# ==========================================
# Player
# ==========================================
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 25

player = pygame.Rect(
    WIDTH // 2 - PLAYER_WIDTH // 2,
    HEIGHT - 70,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)

PLAYER_SPEED = 7

# ==========================================
# Bullet
# ==========================================
BULLET_WIDTH = 6
BULLET_HEIGHT = 20
BULLET_SPEED = 10

bullets = []

# ==========================================
# Enemy
# ==========================================
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 40
ENEMY_SPEED = 3

enemies = []

enemy_spawn_delay = 40
enemy_timer = 0

# ==========================================
# Game Variables
# ==========================================
score = 0
lives = 3

running = True

# ==========================================
# Helper Functions
# ==========================================

def draw_player():

    pygame.draw.rect(screen, BLUE, player)

    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (player.centerx, player.top - 15),
            (player.left, player.top),
            (player.right, player.top),
        ],
    )


def shoot():

    bullet = pygame.Rect(
        player.centerx - BULLET_WIDTH // 2,
        player.top,
        BULLET_WIDTH,
        BULLET_HEIGHT,
    )

    bullets.append(bullet)


def spawn_enemy():

    x = random.randint(0, WIDTH - ENEMY_WIDTH)

    enemy = pygame.Rect(
        x,
        -ENEMY_HEIGHT,
        ENEMY_WIDTH,
        ENEMY_HEIGHT,
    )

    enemies.append(enemy)


def draw_bullets():

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)


def draw_enemies():

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

        pygame.draw.rect(
            screen,
            WHITE,
            enemy,
            2,
        )


def draw_score():

    text = font.render(
        f"Score : {score}",
        True,
        WHITE,
    )

    screen.blit(text, (15, 15))


def draw_lives():

    text = font.render(
        f"Lives : {lives}",
        True,
        WHITE,
    )

    screen.blit(text, (650, 15))
    # ==========================================
# Main Game Loop
# ==========================================

while running:

    clock.tick(FPS)

    enemy_timer += 1

    # ----------------------
    # Events
    # ----------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                shoot()

    # ----------------------
    # Player Movement
    # ----------------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED

    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    # ----------------------
    # Spawn Enemies
    # ----------------------

    if enemy_timer >= enemy_spawn_delay:

        enemy_timer = 0
        spawn_enemy()

    # ----------------------
    # Move Bullets
    # ----------------------

    for bullet in bullets[:]:

        bullet.y -= BULLET_SPEED

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # ----------------------
    # Move Enemies
    # ----------------------

    for enemy in enemies[:]:

        enemy.y += ENEMY_SPEED

        # Enemy reached bottom

        if enemy.top > HEIGHT:

            enemies.remove(enemy)

            lives -= 1

            if lives <= 0:
                running = False

    # ----------------------
    # Bullet Collision
    # ----------------------

    for bullet in bullets[:]:

        for enemy in enemies[:]:

            if bullet.colliderect(enemy):

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy in enemies:
                    enemies.remove(enemy)

                score += 10

                break

    # ----------------------
    # Player Collision
    # ----------------------

    for enemy in enemies[:]:

        if player.colliderect(enemy):

            running = False

    # ----------------------
    # Drawing
    # ----------------------

    screen.fill(BLACK)

    draw_player()

    draw_bullets()

    draw_enemies()

    draw_score()

    draw_lives()

    pygame.display.flip()
    # ==========================================
# Game Over Screen
# ==========================================

screen.fill(BLACK)

game_over = big_font.render(
    "GAME OVER",
    True,
    RED,
)

final_score = font.render(
    f"Final Score : {score}",
    True,
    WHITE,
)

restart = font.render(
    "Press R to Restart or ESC to Exit",
    True,
    GREEN,
)

screen.blit(
    game_over,
    (
        WIDTH // 2 - game_over.get_width() // 2,
        180,
    ),
)

screen.blit(
    final_score,
    (
        WIDTH // 2 - final_score.get_width() // 2,
        270,
    ),
)

screen.blit(
    restart,
    (
        WIDTH // 2 - restart.get_width() // 2,
        330,
    ),
)

pygame.display.update()

waiting = True

while waiting:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            waiting = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                waiting = False

            if event.key == pygame.K_r:

                pygame.quit()

                import os

                os.execl(
                    sys.executable,
                    sys.executable,
                    *sys.argv
                )

pygame.quit()
sys.exit()