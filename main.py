import pygame
from constants import *
from game import Game

FPS = 60

WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("ChessAI")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    clock = pygame.time.Clock()
    run = True
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()

    pygame.quit()


if __name__ == "__main__":
    main()
