import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 30)


def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def random_food():
    return (
        random.randrange(0, WIDTH, GRID_SIZE),
        random.randrange(0, HEIGHT, GRID_SIZE),
    )


snake = [(100, 100)]
direction = (GRID_SIZE, 0)

food = random_food()
score = 0

running = True

while running:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                direction = (GRID_SIZE, 0)

    head = (
        snake[0][0] + direction[0],
        snake[0][1] + direction[1],
    )

    # Collision with wall
    if (
        head[0] < 0
        or head[0] >= WIDTH
        or head[1] < 0
        or head[1] >= HEIGHT
        or head in snake
    ):
        break

    snake.insert(0, head)

    if head == food:
        score += 1
        food = random_food()
    else:
        snake.pop()

    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0], segment[1], GRID_SIZE, GRID_SIZE),
        )

    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], GRID_SIZE, GRID_SIZE),
    )

    draw_text(f"Score: {score}", WHITE, 10, 10)

    pygame.display.update()

# Game Over Screen
screen.fill(BLACK)

draw_text("GAME OVER", RED, 190, 240)
draw_text(f"Final Score: {score}", WHITE, 180, 290)

pygame.display.update()

pygame.time.delay(3000)

pygame.quit()