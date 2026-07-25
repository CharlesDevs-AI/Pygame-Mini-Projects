import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 8
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 12
SPACE = 55

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.SysFont("Arial", 35)
clock = pygame.time.Clock()

board = [[0 for _ in range(3)] for _ in range(3)]
player = 1
game_over = False


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (col * 200 + 100, row * 200 + 100),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )

            elif board[row][col] == 2:
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * 200 + SPACE, row * 200 + SPACE),
                    (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE),
                    CROSS_WIDTH,
                )

                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * 200 + SPACE, row * 200 + 200 - SPACE),
                    (col * 200 + 200 - SPACE, row * 200 + SPACE),
                    CROSS_WIDTH,
                )


def available(row, col):
    return board[row][col] == 0


def mark(row, col, p):
    board[row][col] = p


def full():
    for r in board:
        if 0 in r:
            return False
    return True


def winner(p):

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == p:
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == p:
            return True

    if board[0][0] == board[1][1] == board[2][2] == p:
        return True

    if board[0][2] == board[1][1] == board[2][0] == p:
        return True

    return False


def restart():
    global board, player, game_over
    board = [[0 for _ in range(3)] for _ in range(3)]
    player = 1
    game_over = False


while True:

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()

    if game_over:
        msg = "Press R to Restart"
        text = font.render(msg, True, TEXT_COLOR)
        screen.blit(text, (170, 630))

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                restart()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            x = event.pos[0]
            y = event.pos[1]

            if y >= 600:
                continue

            row = y // 200
            col = x // 200

            if available(row, col):

                mark(row, col, player)

                if winner(player):
                    game_over = True

                elif full():
                    game_over = True

                else:
                    player = 2 if player == 1 else 1

    clock.tick(60)