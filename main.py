import pygame
from constants import *
from game import Game
import datetime

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
    for i in range(1, 5):
        start_time = datetime.datetime.now()
        result = game.move_generation_test(i)
        end_time = datetime.datetime.now()
        time_diff = (end_time - start_time)
        execution_time = time_diff.total_seconds() * 1000
        print('Depth', i, 'moves. Result =', result, 'positions with execution time of', execution_time, 'ms')

    # while run:
    #     clock.tick(FPS)
    #     if game.winner() is not None:
    #         print('\nthe great winner is '+game.winner())
    #         run = False
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:
    #                 pos = pygame.mouse.get_pos()
    #                 row, col = get_row_col_from_mouse(pos)
    #                 game.select(row, col)
    #             elif event.button == 5:
    #                 game.undoMove()
    #     game.update()
    #
    # pygame.quit()


if __name__ == "__main__":
    main()
