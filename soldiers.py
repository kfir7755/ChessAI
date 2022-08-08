from abc import ABC, abstractmethod
import os
import pygame
from constants import *


class Soldier(ABC):
    def __init__(self, row, col, color, png_str):
        self.row = row
        self.col = col
        self.color = color
        if png_str is not None:
            self.png = pygame.image.load(os.path.join('PNGs', png_str))
        else:
            self.png = None

    # @abstractmethod
    # def possible_moves(self, board):
    #     pass


class Pawn(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)
        self.is_first_move = True
        self.made_normal_move = False

    def en_passant(self, board, last_move):
        moves = []
        if last_move is None:
            return moves
        b_row, b_col = last_move[0], last_move[1]
        a_row, a_col = last_move[2], last_move[3]
        color = self.color
        last_move_soldier = board[a_row][a_col]
        if (abs(a_row - b_row) != 2) or not isinstance(last_move_soldier, Pawn):
            return moves
        if not last_move_soldier.is_first_move and not last_move_soldier.made_normal_move and self.row == a_row and\
                abs(a_col-self.col) == 1:
            if color == 'white':
                moves.append((self.row, self.col, a_row-1, a_col))
            if color == 'black':
                moves.append((self.row, self.col, a_row+1, a_col))
        return moves

    def possible_moves(self, board, last_move):
        row, col, color = self.row, self.col, self.color
        mark = []
        if color == 'white':
            moves = [(row, col, row - 1, col), (row, col, row - 2, col), (row, col, row - 1, col + 1), (row, col, row - 1, col - 1)]
            moves += self.en_passant(board, last_move)
            if not self.is_first_move:
                moves.remove((row, col, row - 2, col))
            for move in moves:
                if (move[2] >= N) or (move[2] < 0) or (move[3] >= N) or (move[3] < 0):
                    mark.append(move)
            moves = [move for move in moves if move not in mark]
            if (row, col, row - 1, col) in moves:
                if board[row - 1][col] is not None:
                    moves.remove((row, col, row - 1, col))
            if (row, col, row - 2, col) in moves:
                if board[row - 2][col] is not None:
                    moves.remove((row, col, row - 2, col))
            if (row, col,row - 1, col + 1) in moves:
                if board[row - 1][col + 1] is None:
                    moves.remove((row, col, row - 1, col + 1))
                elif board[row - 1][col + 1].color == 'white':
                    moves.remove((row, col, row - 1, col + 1))
            if (row, col, row - 1, col - 1) in moves:
                if board[row - 1][col - 1] is None:
                    moves.remove((row, col, row - 1, col - 1))
                elif board[row - 1][col - 1].color == 'white':
                    moves.remove((row, col, row - 1, col - 1))
            if (row, col, row - 2, col) in moves and (row, col, row - 1, col) not in moves:
                moves.remove((row, col, row - 2, col))
        elif color == 'black':
            moves = [(row, col, row + 1, col + 1), (row, col, row + 2, col), (row, col, row + 1, col), (row, col, row + 1, col - 1)]
            moves += self.en_passant(board, last_move)
            if not self.is_first_move:
                moves.remove((row, col, row + 2, col))
            for move in moves:
                if (move[2] >= N) or (move[2] < 0) or (move[3] >= N) or (move[3] < 0):
                    mark.append(move)
            moves = [move for move in moves if move not in mark]
            if (row, col, row + 1, col + 1) in moves:
                if board[row + 1][col + 1] is None:
                    moves.remove((row, col, row + 1, col + 1))
                elif board[row + 1][col + 1].color == 'black':
                    moves.remove((row, col, row + 1, col + 1))
            if (row, col, row + 1, col) in moves:
                if board[row + 1][col] is not None:
                    moves.remove((row, col, row + 1, col))
            if (row, col, row + 2, col) in moves:
                if board[row + 2][col] is not None:
                    moves.remove((row, col, row + 2, col))
            if (row, col, row + 1, col - 1) in moves:
                if board[row + 1][col - 1] is None:
                    moves.remove((row, col, row + 1, col - 1))
                elif board[row + 1][col - 1].color == 'black':
                    moves.remove((row, col, row + 1, col - 1))
            if (row, col, row + 2, col) in moves and (row, col, row + 1, col) not in moves:
                moves.remove((row, col, row + 2, col))
        # if check:
        #     # need to make a mark, to remove 1 after 1
        #     for move in moves:
        # #         if still threatening, remove it
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
                    moves.append((row, col, row + i, col + i))
                elif board[row + i][col + i].color is not color:
                    moves.append((row, col, row + i, col + i))
                    break
                elif board[row + i][col + i].color is color:
                    break
        for i in range(1, 8):
            if row - i >= 0 and col - i >= 0:
                if board[row - i][col - i] is None:
                    moves.append((row, col, row - i, col - i))
                elif board[row - i][col - i].color is not color:
                    moves.append((row, col, row - i, col - i))
                    break
                elif board[row - i][col - i].color is color:
                    break
        for i in range(1, 8):
            if row - i >= 0 and col + i < N:
                if board[row - i][col + i] is None:
                    moves.append((row, col, row - i, col + i))
                elif board[row - i][col + i].color is not color:
                    moves.append((row, col, row - i, col + i))
                    break
                elif board[row - i][col + i].color is color:
                    break
        for i in range(1, 8):
            if row + i < N and col - i >= 0:
                if board[row + i][col - i] is None:
                    moves.append((row, col, row + i, col - i))
                elif board[row + i][col - i].color is not color:
                    moves.append((row, col, row + i, col - i))
                    break
                elif board[row + i][col - i].color is color:
                    break
        return moves


class King(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        row, col, color = self.row, self.col, self.color
        moves = [(row, col, row, col + 1), (row, col, row - 1, col + 1), (row, col, row - 1, col),
                 (row, col, row - 1, col - 1), (row, col, row, col - 1),
                 (row, col, row + 1, col - 1), (row, col, row + 1, col), (row, col, row + 1, col + 1)]
        mark = []
        for move in moves:
            if (move[2] >= N) or (move[2] < 0) or (move[3] >= N) or (move[3] < 0):
                mark.append(move)
        moves = [move for move in moves if move not in mark]
        mark = []
        for move in moves:
            if board[move[2]][move[3]] is not None:
                if board[move[2]][move[3]].color is color:
                    mark.append(move)
        moves = [move for move in moves if move not in mark]
        return moves


class Knight(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        row, col, color = self.row, self.col, self.color
        moves = [(row, col, row - 1, col - 2), (row, col, row - 2, col - 1), (row, col, row - 2, col + 1),
                 (row, col, row - 1, col + 2), (row, col, row + 1, col + 2),
                 (row, col, row + 2, col + 1), (row, col, row + 2, col - 1), (row, col, row + 1, col - 2)]
        mark = []
        for move in moves:
            if (move[2] >= N) or (move[2] < 0) or (move[3] >= N) or (move[3] < 0):
                mark.append(move)
        moves = [move for move in moves if move not in mark]
        mark = []
        for move in moves:
            if board[move[2]][move[3]] is not None:
                if board[move[2]][move[3]].color is color:
                    mark.append(move)
        moves = [move for move in moves if move not in mark]
        return moves


class Queen(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        rook = Rook(self.row, self.col, self.color, None)
        bishop = Bishop(self.row, self.col, self.color, None)
        moves = rook.possible_moves(board)
        moves += bishop.possible_moves(board)
        return moves


class Rook(Soldier):
    def __init__(self, row, col, color, png_str):
        super().__init__(row, col, color, png_str)

    def possible_moves(self, board):
        row, col, color = self.row, self.col, self.color
        moves = []
        for i in range(1, 8):
            if row + i < N:
                if board[row + i][col] is None:
                    moves.append((row, col, row + i, col))
                elif board[row + i][col].color is not color:
                    moves.append((row, col, row + i, col))
                    break
                elif board[row + i][col].color is color:
                    break
        for i in range(1, 8):
            if row - i >= 0:
                if board[row - i][col] is None:
                    moves.append((row, col, row - i, col))
                elif board[row - i][col].color is not color:
                    moves.append((row, col, row - i, col))
                    break
                elif board[row - i][col].color is color:
                    break
        for i in range(1, 8):
            if col + i < N:
                if board[row][col + i] is None:
                    moves.append((row, col, row, col + i))
                elif board[row][col + i].color is not color:
                    moves.append((row, col, row, col + i))
                    break
                elif board[row][col + i].color is color:
                    break
        for i in range(1, 8):
            if col - i >= 0:
                if board[row][col - i] is None:
                    moves.append((row, col, row, col - i))
                elif board[row][col - i].color is not color:
                    moves.append((row, col, row, col - i))
                    break
                elif board[row][col - i].color is color:
                    break
        return moves
