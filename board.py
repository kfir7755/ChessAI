from constants import *
from soldiers import *


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.fallen_king = None
        self.last_move = None

    def __getitem__(self, board):
        return self.board

    def move_en_passant(self, cur_row, cur_col, next_row, next_col):
        self.board[next_row][next_col], self.board[cur_row][cur_col] = self.board[cur_row][cur_col], None
        if cur_row > next_row:
            self.board[next_row + 1][next_col] = None
        else:
            self.board[next_row - 1][next_col] = None
        self.last_move = ((cur_row, cur_col), (next_row, next_col))
        return True

    def move(self, cur_row, cur_col, next_row, next_col, moves):
        if (next_row, next_col) in moves:
            soldier = self.board[cur_row][cur_col]
            soldier.row, soldier.col = next_row, next_col
            if isinstance(soldier, Pawn):
                soldier.is_first_move = False
                if soldier.color == 'white' and next_row == 0:
                    self.board[cur_row][cur_col] = Queen(next_row, next_col, 'white', 'white_queen.png')
                if soldier.color == 'black' and next_row == 7:
                    self.board[cur_row][cur_col] = Queen(next_row, next_col, 'black', 'black_queen.png')
                if self.board[next_row][next_col] is None and next_col != cur_col:
                    self.move_en_passant(cur_row, cur_col, next_row, next_col)
                    return True
                elif (next_row, next_col) != (cur_row - 2, cur_col) and\
                        (next_row, next_col) != (cur_row + 2, cur_col):
                    soldier.made_normal_move = True
            if self.board[next_row][next_col] is not None:
                if isinstance(self.board[next_row][next_col], King):
                    self.fallen_king = self.board[next_row][next_col].color
            self.board[next_row][next_col], self.board[cur_row][cur_col] = self.board[cur_row][cur_col], None
            self.last_move = ((cur_row, cur_col), (next_row, next_col))
            return True
        return False

    @staticmethod
    def draw_squares(win):
        win.fill(GREEN)
        for row in range(N):
            for col in range(row % 2, N, 2):
                pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win):
        for row in range(N):
            for col in range(N):
                if self.board[row][col] is not None:
                    image = self.board[row][col].png
                    win.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def create_board(self):
        board = [[0 for _ in range(N)] for _ in range(N)]
        board[0][0] = Rook(0, 0, 'black', 'black_rook.png')
        board[0][1] = Knight(0, 1, 'black', 'black_knight.png')
        board[0][2] = Bishop(0, 2, 'black', 'black_bishop.png')
        board[0][3] = Queen(0, 3, 'black', 'black_queen.png')
        board[0][4] = King(0, 4, 'black', 'black_king.png')
        board[0][5] = Bishop(0, 5, 'black', 'black_bishop.png')
        board[0][6] = Knight(0, 6, 'black', 'black_knight.png')
        board[0][7] = Rook(0, 7, 'black', 'black_rook.png')
        for j in range(N):
            board[1][j] = Pawn(1, j, 'black', 'black_pawn.png')
        for row in range(2, 6):
            for col in range(N):
                board[row][col] = None
        for j in range(N):
            board[6][j] = Pawn(6, j, 'white', 'white_pawn.png')
        board[7][0] = Rook(7, 0, 'white', 'white_rook.png')
        board[7][1] = Knight(7, 1, 'white', 'white_knight.png')
        board[7][2] = Bishop(7, 2, 'white', 'white_bishop.png')
        board[7][3] = Queen(7, 3, 'white', 'white_queen.png')
        board[7][4] = King(7, 4, 'white', 'white_king.png')
        board[7][5] = Bishop(7, 5, 'white', 'white_bishop.png')
        board[7][6] = Knight(7, 6, 'white', 'white_knight.png')
        board[7][7] = Rook(7, 7, 'white', 'white_rook.png')
        self.board = board
