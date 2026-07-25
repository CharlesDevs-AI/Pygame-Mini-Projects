import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Colors
SKY = (135, 206, 235)
GREEN = (34, 177, 76)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Bird
bird = pygame.Rect(100, 300, 30, 30)
velocity = 0
gravity = 0.5
jump_strength = -8

# Pipes
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 4

pipes = []

PIPE_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_EVENT, 1500)

score = 0

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == PIPE_EVENT:
            h = random.randint(120, 420)

            top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, h)
            bottom = pygame.Rect(
                WIDTH,
                h + PIPE_GAP,
                PIPE_WIDTH,
                HEIGHT - h - PIPE_GAP,
            )

            pipes.append([top, bottom, False])

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                velocity = jump_strength

    # Bird Physics
    velocity += gravity
    bird.y += velocity

    # Background
    screen.fill(SKY)

    # Bird
    pygame.draw.ellipse(screen, YELLOW, bird)

    # Pipes
    for pipe in pipes[:]:

        top, bottom, passed = pipe

        top.x -= PIPE_SPEED
        bottom.x -= PIPE_SPEED

        pygame.draw.rect(screen, GREEN, top)
        pygame.draw.rect(screen, GREEN, bottom)

        # Collision
        if bird.colliderect(top) or bird.colliderect(bottom):
            running = False

        # Score
        if not passed and top.right < bird.left:
            score += 1
            pipe[2] = True

        # Remove Off Screen
        if top.right < 0:
            pipes.remove(pipe)

    # Ground / Sky Collision
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        running = False

    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

# Game Over
screen.fill(SKY)

game_over = font.render("GAME OVER", True, WHITE)
score_text = font.render(f"Final Score : {score}", True, WHITE)

screen.blit(game_over, (150, 280))
screen.blit(score_text, (145, 330))

pygame.display.flip()

pygame.time.wait(3000)

pygame.quit()