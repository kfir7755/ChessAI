from constants import *
from soldiers import *
import os


class Square:
    def __init__(self, x, y, soldier, color, soldier_png):
        self.x = x
        self.y = y
        if soldier is not None:
            self.soldier = soldier(self, color, soldier_png)
        else:
            self.soldier = None

    def set_soldier(self, soldier):
        self.soldier = soldier

    def get_soldier(self):
        return self.soldier


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None

    def __getitem__(self, board):
        return self.board

    def draw_squares(self, win):
        win.fill(GREEN)
        for row in range(N):
            for col in range(row % 2, N, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for row in range(N):
            for col in range(N):
                if self.board[row][col].soldier is not None:
                    image = self.board[row][col].soldier.png
                    win.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def create_board(self):
        board = [[0 for _ in range(N)] for _ in range(N)]
        board[0][0] = Square(0, 0, Rook, 'black', 'black_rook.png')
        board[0][1] = Square(0, 1, Knight, 'black', 'black_knight.png')
        board[0][2] = Square(0, 2, Bishop, 'black', 'black_bishop.png')
        board[0][3] = Square(0, 3, Queen, 'black', 'black_queen.png')
        board[0][4] = Square(0, 4, King, 'black', 'black_king.png')
        board[0][5] = Square(0, 5, Bishop, 'black', 'black_bishop.png')
        board[0][6] = Square(0, 6, Knight, 'black', 'black_knight.png')
        board[0][7] = Square(0, 7, Rook, 'black', 'black_rook.png')
        for j in range(N):
            board[1][j] = Square(1, j, Pawn, 'black', 'black_pawn.png')
        for row in range(2, 6):
            for col in range(N):
                board[row][col] = Square(row, col, None, None, None)
        for j in range(N):
            board[6][j] = Square(6, j, Pawn, 'white', 'white_pawn.png')
        board[7][0] = Square(0, 0, Rook, 'white', 'white_rook.png')
        board[7][1] = Square(0, 1, Knight, 'white', 'white_knight.png')
        board[7][2] = Square(0, 2, Bishop, 'white', 'white_bishop.png')
        board[7][3] = Square(0, 3, Queen, 'white', 'white_queen.png')
        board[7][4] = Square(0, 4, King, 'white', 'white_king.png')
        board[7][5] = Square(0, 5, Bishop, 'white', 'white_bishop.png')
        board[7][6] = Square(0, 6, Knight, 'white', 'white_knight.png')
        board[7][7] = Square(0, 7, Rook, 'white', 'white_rook.png')
        self.board = board
