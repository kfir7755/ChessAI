from soldiers import *
from copy import copy


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = []
        self.counter = 0
        self.create_board()
        self.turn = 'white'
        self.win = win
        self.moves = []
        self.all_possible_moves = []
        self.selected_piece = None
        self.last_move = None
        self.threatening_moves_available = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

    # def winner(self):
    #     if self.fallen_king is not None:
    #         if self.fallen_king == 'black':
    #             return 'white'
    #         else:
    #             return 'black'
    #     return None

    def winner(self):
        if self.all_possible_moves is None:
            if self.turn == 'black':
                return 'white'
            else:
                return 'black'
        return None

    def update(self):
        self.draw_squares(self.win)
        if len(self.moves) > 0:
            self.draw_circles()
        if len(self.threatening_moves_available) > 0:
            self.draw_threats()
        self.draw_pieces(self.win)
        pygame.display.update()

    def select(self, row, col):
        if self.counter == 0:
            self.calc_all_possible_moves()
            self.counter = 1
        if self.selected is not None:
            cur_row, cur_col = self.selected
            result = self.move(cur_row, cur_col, row, col)
            self.selected = None
            if not result:
                self.select(row, col)
            elif result:
                self.moves = []
                temp = self.turn
                self.turn = 'black' if temp == 'white' else 'white'
                self.threatening_moves_check()
                self.calc_all_possible_moves()
        else:
            self.selected = row, col
            if self.board[row][col] is not None:
                if self.board[row][col].color == self.turn:
                    soldier = self.board[row][col]
                    if not isinstance(soldier, Pawn):
                        self.moves = soldier.possible_moves(self.board)
                    else:
                        self.moves = soldier.possible_moves(self.board, self.last_move)
                    self.fix_moves()
                else:
                    self.moves = []

    def move(self, cur_row, cur_col, next_row, next_col):
        if (cur_row, cur_col, next_row, next_col) in self.moves:
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
                elif (next_row, next_col) != (cur_row - 2, cur_col) and \
                        (next_row, next_col) != (cur_row + 2, cur_col):
                    soldier.made_normal_move = True
            if (cur_row, cur_col) == self.white_king_location:
                self.white_king_location = next_row, next_col
            if (cur_row, cur_col) == self.black_king_location:
                self.black_king_location = next_row, next_col
            self.board[next_row][next_col], self.board[cur_row][cur_col] = self.board[cur_row][cur_col], None
            self.last_move = (cur_row, cur_col, next_row, next_col)
            return True
        return False

    def fix_moves(self):
        king_loc = self.white_king_location if self.turn == 'white' else self.black_king_location
        king_move = king_loc
        valid_moves = []
        isKing = False
        if len(self.moves) > 0:
            isKing = (self.moves[0][0], self.moves[0][1]) == king_loc
        if len(self.threatening_moves_available) == 0 and not isKing:
            return
        for move in self.moves:
            if isKing:
                king_move = move[2], move[3]
                temp = self.threatening_moves_available
                if self.turn == 'white':
                    self.white_king_location = king_move
                else:
                    self.black_king_location = king_move
                self.threatening_moves_check()
                if len(self.threatening_moves_available) == 0:
                    valid_moves.append(move)
                    continue
            soldier = copy(self.board[move[2]][move[3]])
            self.board[move[2]][move[3]], self.board[move[0]][move[1]] = self.board[move[0]][move[1]], None
            before_last_move = self.last_move
            self.last_move = move
            for threatening_move in self.threatening_moves_available:
                if isinstance(self.board[threatening_move[0]][threatening_move[1]], Pawn):
                    possible_moves = self.board[threatening_move[0]][threatening_move[1]]. \
                        possible_moves(self.board, self.last_move)
                else:
                    possible_moves = self.board[threatening_move[0]][threatening_move[1]].possible_moves(self.board)
                valid = True
                for enemy_threatening_move in possible_moves:
                    if (enemy_threatening_move[2], enemy_threatening_move[3]) == king_move:
                        valid = False
                if valid:
                    valid_moves.append(move)
            if isKing:
                self.threatening_moves_available = temp
                king_loc = move[0], move[1]
                if self.turn == 'white':
                    self.white_king_location = king_loc
                else:
                    self.black_king_location = king_loc
            self.board[move[0]][move[1]], self.board[move[2]][move[3]] = self.board[move[2]][move[3]], soldier
            self.last_move = before_last_move
        self.moves = valid_moves

    def fix_all_possible_moves(self):
        king_loc = self.white_king_location if self.turn == 'white' else self.black_king_location
        valid_moves = []
        king_move = king_loc
        for move in self.all_possible_moves:
            isKing = (move[0], move[1]) == king_loc
            if isKing:
                king_move = move[2], move[3]
                temp = self.threatening_moves_available
                if self.turn == 'white':
                    self.white_king_location = king_move
                else:
                    self.black_king_location = king_move
                self.threatening_moves_check()
            if len(self.threatening_moves_available) == 0:
                if self.turn == 'white':
                    self.white_king_location = king_loc
                else:
                    self.black_king_location = king_loc
                valid_moves.append(move)
                continue
            soldier = copy(self.board[move[2]][move[3]])
            self.board[move[2]][move[3]], self.board[move[0]][move[1]] = self.board[move[0]][move[1]], None
            before_last_move = self.last_move
            self.last_move = move
            for threatening_move in self.threatening_moves_available:
                if isinstance(self.board[threatening_move[0]][threatening_move[1]], Pawn):
                    possible_moves = self.board[threatening_move[0]][threatening_move[1]]. \
                        possible_moves(self.board, self.last_move)
                else:
                    possible_moves = self.board[threatening_move[0]][threatening_move[1]].possible_moves(self.board)
                valid = True
                for enemy_threatening_move in possible_moves:
                    if (enemy_threatening_move[2], enemy_threatening_move[3]) == king_move:
                        valid = False
                if valid:
                    valid_moves.append(move)
                if isKing:
                    self.threatening_moves_available = temp
                    if self.turn == 'white':
                        self.white_king_location = king_loc
                    else:
                        self.black_king_location = king_loc
            self.board[move[0]][move[1]], self.board[move[2]][move[3]] = self.board[move[2]][move[3]], soldier
            self.last_move = before_last_move
        self.all_possible_moves = valid_moves

    def threatening_moves_check(self):
        self.threatening_moves_available = []
        king_loc = self.white_king_location if self.turn == 'white' else self.black_king_location
        squares_to_check = self.find_opt_threatening_squares(*king_loc)
        for square in squares_to_check:
            if self.board[square[0]][square[1]] is not None:
                if self.board[square[0]][square[1]].color != self.turn:
                    soldier = self.board[square[0]][square[1]]
                    possible_moves = soldier.possible_moves(self.board, self.last_move) if isinstance(soldier, Pawn) \
                        else soldier.possible_moves(self.board)
                    for move in possible_moves:
                        if (move[2], move[3]) == king_loc:
                            self.threatening_moves_available.append(move)

    def move_en_passant(self, cur_row, cur_col, next_row, next_col):
        self.board[next_row][next_col], self.board[cur_row][cur_col] = self.board[cur_row][cur_col], None
        if cur_row > next_row:
            self.board[next_row + 1][next_col] = None
        else:
            self.board[next_row - 1][next_col] = None
        self.last_move = (cur_row, cur_col, next_row, next_col)
        return True

    def calc_all_possible_moves(self):
        self.all_possible_moves = []
        for row in range(N):
            for col in range(N):
                if self.board[row][col] is not None:
                    if self.board[row][col].color == self.turn:
                        if isinstance(self.board[row][col], Pawn):
                            self.all_possible_moves += self.board[row][col].possible_moves(self.board, self.last_move)
                        else:
                            self.all_possible_moves += self.board[row][col].possible_moves(self.board)
        self.fix_all_possible_moves()
        if len(self.all_possible_moves) == 0:
            self.all_possible_moves = None

    def draw_circles(self):
        cur_row, cur_col = self.selected
        pygame.draw.rect(self.win, BLUE, (cur_col * SQUARE_SIZE, cur_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for move in self.moves:
            row, col = move[2], move[3]
            yellow = YELLOW_FOR_WHITE if (col + row) % 2 == 0 else YELLOW_FOR_GREEN
            grey = GREY_FOR_WHITE if (col + row) % 2 == 0 else GREY_FOR_GREEN
            if self.board[row][col] is None:
                pygame.draw.circle(self.win, grey,
                                   [col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2],
                                   SQUARE_SIZE // 6, 0)
            else:
                pygame.draw.rect(self.win, yellow, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_threats(self):
        if len(self.threatening_moves_available) > 0:
            for threatening_move in self.threatening_moves_available:
                if self.turn != self.board[threatening_move[0]][threatening_move[1]].color:
                    pygame.draw.rect(self.win, RED, (threatening_move[1] * SQUARE_SIZE,
                                                     threatening_move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def draw_squares(win):
        win.fill(GREEN)
        for row in range(N):
            for col in range(row % 2, N, 2):
                pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def find_opt_threatening_squares(row, col):
        squares = [(row - 1, col - 2), (row - 2, col - 1), (row - 2, col + 1), (row - 1, col + 2), (row + 1, col + 2),
                   (row + 2, col + 1), (row + 2, col - 1), (row + 1, col - 2), (row - 1, col), (row - 2, col),
                   (row - 3, col), (row - 4, col), (row - 5, col), (row - 6, col), (row - 7, col), (row + 1, col),
                   (row + 2, col), (row + 3, col), (row + 4, col), (row + 5, col), (row + 6, col), (row + 7, col),
                   (row, col + 1), (row, col + 2), (row, col + 3), (row, col + 4), (row, col + 5), (row, col + 6),
                   (row, col + 7), (row, col - 1), (row, col - 2), (row, col - 3), (row, col - 4), (row, col - 5),
                   (row, col - 6), (row, col - 7), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3),
                   (row + 4, col + 4), (row + 5, col + 5), (row + 6, col + 6), (row + 7, col + 7), (row - 1, col - 1),
                   (row - 2, col - 2), (row - 3, col - 3), (row - 4, col - 4), (row - 5, col - 5), (row - 6, col - 6),
                   (row - 7, col - 7), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3), (row - 4, col + 4),
                   (row - 5, col + 5), (row - 6, col + 6), (row - 7, col + 7), (row + 1, col - 1), (row + 2, col - 2),
                   (row + 3, col - 3), (row + 4, col - 4), (row + 5, col - 5), (row + 6, col - 6), (row + 7, col - 7)]
        squares = [square for square in squares if 0 <= square[0] < N and 0 <= square[1] < N]
        return squares

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
