import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

left_paddle = pygame.Rect(30, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
BALL_SIZE = 15
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                   HEIGHT // 2 - BALL_SIZE // 2,
                   BALL_SIZE,
                   BALL_SIZE)

ball_speed_x = 5
ball_speed_y = 5

# Score
left_score = 0
right_score = 0

font = pygame.font.SysFont("Arial", 36)

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()

    # Left Paddle (W,S)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Right Paddle (UP,DOWN)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Top/Bottom Collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle Collision
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Left Miss
    if ball.left <= 0:
        right_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1

    # Right Miss
    if ball.right >= WIDTH:
        left_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= -1

    # Draw
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)

    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()