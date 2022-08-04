from board import *
from constants import *
import pygame


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.board.create_board()
        self.turn = 'white'
        self.win = win
        self.moves = []

    def winner(self):
        if self.board.fallen_king is not None:
            if self.board.fallen_king is 'black':
                return 'white'
            else:
                return 'black'
        return None

    def update(self):
        self.board.draw_squares(self.win)
        if len(self.moves) > 0:
            self.draw_circles()
        self.board.draw_pieces(self.win)
        pygame.display.update()

    def select(self, row, col):
        if self.selected is not None:
            cur_row, cur_col = self.selected
            result = self.board.move(cur_row, cur_col, row, col, self.moves)
            self.selected = None
            if not result:
                self.select(row, col)
            elif result:
                self.moves = []
                temp = self.turn
                self.turn = 'black' if temp == 'white' else 'white'
        else:
            self.selected = row, col
            if self.board.board[row][col] is not None:
                if self.board.board[row][col].color == self.turn:
                    soldier = self.board.board[row][col]
                    self.moves = soldier.possible_moves(self.board.board)
                else:
                    self.moves = []

    def draw_circles(self):
        cur_row, cur_col = self.selected
        pygame.draw.rect(self.win, BLUE, (cur_col * SQUARE_SIZE, cur_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for move in self.moves:
            row, col = move[0], move[1]
            yellow = YELLOW_FOR_WHITE if (col + row) % 2 == 0 else YELLOW_FOR_GREEN
            grey = GREY_FOR_WHITE if (col + row) % 2 == 0 else GREY_FOR_GREEN
            if self.board.board[row][col] is None:
                pygame.draw.circle(self.win, grey,
                                   [col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2],
                                   SQUARE_SIZE // 6, 0)
            else:
                pygame.draw.rect(self.win, yellow, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
