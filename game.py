from board import *
from constants import *
import pygame


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
            cur_row, cur_col = self.selected
            result = self.board.move(cur_row, cur_col, row, col)
            self.selected = None
            if not result:
                self.select(row, col)
        else:
            self.selected = row, col

    # def select(self, row, col, moves=None):
    #     if self.selected is not None:
    #         cur_row, cur_col = self.selected
    #         result = self.board.move(cur_row, cur_col, row, col, moves)
    #         self.selected = None
    #         if not result:
    #             self.select(row, col)
    #     else:
    #         self.selected = row, col
    #         if self.board[row][col] is not None:
    #             moves = self.board[row][col].possible_moves(self.board)
