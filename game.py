from board import *
from constants import *


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.board.create_board()
        self.turn = WHITE
        self.win = win

    def update(self):
        self.board.draw_squares(self.win)
        pygame.display.update()

    def select(self, row, col):
        if self.selected is not None:
            print(self.selected)
            cur_row, cur_col = self.selected
            self.board.move(cur_row, cur_col, row, col)
            self.selected = None
        #     result = self.move(row, col)
        #     if not result:
        #         self.selected = None
        #         self.select(row, col)
        # soldier = self.board[row][col]
        else:
            self.selected = row, col

    def move(self, row, col):
        return True
