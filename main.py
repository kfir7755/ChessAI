import pygame
from constants import *
from board import Board

FPS = 60

WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("ChessAI")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = x // SQUARE_SIZE
    col = y // SQUARE_SIZE
    return row, col


def main():
    clock = pygame.time.Clock()
    run = True
    board = Board()
    board.create_board()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                soldier = board[row][col].get_soldier()
                # soldier.move(4, 3, board)
        board.draw_squares(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
