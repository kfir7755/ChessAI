from abc import ABC, abstractmethod
import os
import pygame
from constants import N


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
        row, col, color = self.row, self.col, self.color
        mark = []
        if color == 'white':
            moves = [(row - 1, col), (row - 2, col), (row - 1, col + 1), (row - 1, col - 1)]
            if not self.is_first_move:
                moves.remove((row - 2, col))
            for move in moves:
                if (move[0] >= N) or (move[0] < 0) or (move[1] >= N) or (move[1] < 0):
                    mark.append(move)
            moves = [move for move in moves if move not in mark]
            if (row - 1, col) in moves:
                if board[row - 1][col] is not None:
                    moves.remove((row - 1, col))
            if (row - 2, col) in moves:
                if board[row - 2][col] is not None:
                    moves.remove((row - 2, col))
            if (row - 1, col + 1) in moves:
                if board[row - 1][col + 1] is None:
                    moves.remove((row - 1, col + 1))
                elif board[row - 1][col + 1].color == 'white':
                    moves.remove((row - 1, col + 1))
            if (row - 1, col - 1) in moves:
                if board[row - 1][col - 1] is None:
                    moves.remove((row - 1, col - 1))
                elif board[row - 1][col - 1].color == 'white':
                    moves.remove((row - 1, col - 1))
            if (row - 2, col) in moves and (row - 1, col) not in moves:
                moves.remove((row - 2, col))
        elif color == 'black':
            moves = [(row + 1, col + 1), (row + 2, col), (row + 1, col), (row + 1, col - 1)]
            if not self.is_first_move:
                moves.remove((row + 2, col))
            for move in moves:
                if (move[0] >= N) or (move[0] < 0) or (move[1] >= N) or (move[1] < 0):
                    mark.append(move)
            moves = [move for move in moves if move not in mark]
            if (row + 1, col + 1) in moves:
                if board[row + 1][col + 1] is None:
                    moves.remove((row + 1, col + 1))
                elif board[row + 1][col + 1].color == 'black':
                    moves.remove((row + 1, col + 1))
            if (row + 1, col) in moves:
                if board[row + 1][col] is not None:
                    moves.remove((row + 1, col))
            if (row + 2, col) in moves:
                if board[row + 2][col] is not None:
                    moves.remove((row + 2, col))
            if (row + 1, col - 1) in moves:
                if board[row + 1][col - 1] is None:
                    moves.remove((row + 1, col - 1))
                elif board[row + 1][col - 1].color == 'black':
                    moves.remove((row + 1, col - 1))
            if (row + 2, col) in moves and (row + 1, col) not in moves:
                moves.remove((row + 2, col))
        return moves


class Bishop(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        row, col, color = self.row, self.col, self.color
        moves = []
        for i in range(1, 8):
            if row + i < N and col + i < N:
                if board[row + i][col + i] is None:
                    moves.append((row + i, col + i))
                elif board[row + i][col + i].color is not color:
                    moves.append((row + i, col + i))
                    break
                elif board[row + i][col + i].color is color:
                    break
        for i in range(1, 8):
            if row - i >= 0 and col - i >= 0:
                if board[row - i][col - i] is None:
                    moves.append((row - i, col - i))
                elif board[row - i][col - i].color is not color:
                    moves.append((row - i, col - i))
                    break
                elif board[row - i][col - i].color is color:
                    break
        for i in range(1, 8):
            if row - i >= 0 and col + i < N:
                if board[row - i][col + i] is None:
                    moves.append((row - i, col + i))
                elif board[row - i][col + i].color is not color:
                    moves.append((row - i, col + i))
                    break
                elif board[row - i][col + i].color is color:
                    break
        for i in range(1, 8):
            if row + i < N and col - i >= 0:
                if board[row + i][col - i] is None:
                    moves.append((row + i, col - i))
                elif board[row + i][col - i].color is not color:
                    moves.append((row + i, col - i))
                    break
                elif board[row + i][col - i].color is color:
                    break
        return moves


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
