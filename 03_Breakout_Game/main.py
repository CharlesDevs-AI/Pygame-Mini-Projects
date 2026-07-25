import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("Arial", 30)

# Paddle
paddle = pygame.Rect(350, 560, 100, 15)
PADDLE_SPEED = 8

# Ball
ball = pygame.Rect(390, 300, 15, 15)
ball_dx = 5
ball_dy = -5

# Bricks
bricks = []

for row in range(5):
    for col in range(10):
        brick = pygame.Rect(
            col * 75 + 20,
            row * 35 + 40,
            65,
            25
        )
        bricks.append(brick)

score = 0

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED

    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx *= -1

    if ball.top <= 0:
        ball_dy *= -1

    if ball.colliderect(paddle):
        ball_dy *= -1

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy *= -1
            score += 10
            break

    if ball.bottom >= HEIGHT:
        running = False

    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    score_text = font.render(f"Score : {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    if len(bricks) == 0:
        win = font.render("YOU WIN!", True, GREEN)
        screen.blit(win, (320, 280))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    pygame.display.update()

screen.fill(BLACK)

game_over = font.render("GAME OVER", True, RED)
screen.blit(game_over, (300, 280))

pygame.display.update()

pygame.time.wait(3000)

pygame.quit()