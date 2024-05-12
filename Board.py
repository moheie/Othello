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
        # Initialize the game board with starting positions
        board = [[EMPTY for _ in range(8)] for _ in range(8)]
        mid = len(board) // 2
        board[mid - 1][mid - 1] = WHITE
        board[mid][mid] = WHITE
        board[mid - 1][mid] = BLACK
        board[mid][mid - 1] = BLACK
        return board
    def display_board(self):
        # Display the current game board state
        for row in self.board:
            print(row)
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
        if self.board[row][col] != EMPTY:
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
                        return True  # Move is valid
                    r += dr
                    c += dc

        return False  # No valid move found in any direction

    def make_move(self, row, col, player_color):
        # Make a move on the board
        if self.is_valid_move(row, col, player_color):
            self.board[row][col] = player_color
            self.flip_pieces(row, col, player_color)

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
        return not black_moves and not white_moves