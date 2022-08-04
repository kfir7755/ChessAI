from abc import ABC, abstractmethod
import os
import pygame


class Soldier(ABC):
    def __init__(self, row, col, color, png_str):
        self.row = row
        self.col = col
        self.color = color
        if png_str is not None:
            self.png = pygame.image.load(os.path.join('PNGs', png_str))
        else:
            self.png = None

    @abstractmethod
    def possible_moves(self, board):
        pass


class Pawn(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)
        self.is_first_move = True

    def possible_moves(self, board):
        pass


class Bishop(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        pass


class King(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        pass


class Knight(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        pass


class Queen(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        pass


class Rook(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        pass
