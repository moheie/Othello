import pygame
import sys
from pygame.locals import *
import random

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class Board:
    def __init__(self):
        self.board = self.initialize_board()

    def initialize_board(self):
        board = [[EMPTY for _ in range(8)] for _ in range(8)]
        board[3][3] = board[4][4] = WHITE
        board[3][4] = board[4][3] = BLACK
        return board

    def display_board(self):
        # Display the game board
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(i, end=' ')
            for col in row:
                print(col, end=' ')
            print()

    def get_valid_moves(self, player_color):
        # Get a list of valid moves for the given player color
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player_color):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, row, col, player_color):
        # Check if a move is valid for the given player color
        if self.board[row][col] != EMPTY or not (0 <= row < 8 and 0 <= col < 8):
            return False  # Square is not empty

        # Directions to check for opponent's pieces
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != EMPTY and self.board[r][c] != player_color:
                # Found an opponent's piece in this direction
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == EMPTY:
                        break
                    if self.board[r][c] == player_color:
                        return True
                    r += dr
                    c += dc

        return False

    def make_move(self, row, col, player_color):
        # Make a move on the board for the given player color
        if not self.is_valid_move(row, col, player_color):
            return False

        self.board[row][col] = player_color
        self.flip_pieces(row, col, player_color)
        return True

    def flip_pieces(self, row, col, player_color):
        # Implement logic to flip opponent's pieces when a move is made
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != EMPTY and self.board[r][c] != player_color:
                # Found an opponent's piece in this direction
                to_flip = []
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == EMPTY:
                        break
                    if self.board[r][c] == player_color:
                        for flip_row, flip_col in to_flip:
                            self.board[flip_row][flip_col] = player_color
                        break
                    to_flip.append((r, c))
                    r += dr
                    c += dc

    def is_game_over(self):
        # Check if the game is over (no valid moves for both players)
        black_moves = any(self.is_valid_move(row, col, BLACK) for row in range(8) for col in range(8))
        white_moves = any(self.is_valid_move(row, col, WHITE) for row in range(8) for col in range(8))
        black_count, white_count = self.count_pieces()
        return not black_moves and not white_moves or black_count == 0 or white_count == 0

    def count_pieces(self):
        # Count the number of black and white pieces on the board
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        return black_count, white_count

    def copy(self):
        # Create a copy of the board
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board

    def is_board_full(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

    def get_winner(self):
        black_count, white_count = self.count_pieces()
        if black_count > white_count:
            return BLACK
        elif white_count > black_count:
            return WHITE
        else:
            return None  # It's a tie

    def reset_board(self):
        self.board = self.initialize_board()

    def get_board_state(self):
        return self.board

    def set_board_state(self, board):
        self.board = board

    def get_possible_moves(self, player_color):
        return self.get_valid_moves(player_color)

    def execute_move(self, row, col, player_color):
        return self.make_move(row, col, player_color)

    def get_board_size(self):
        return len(self.board)

    def get_score(self):
        black_count, white_count = self.count_pieces()
        return black_count, white_count