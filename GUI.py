import pygame
import sys
from pygame.locals import *
import random

from Board import Board
from GameController import GameController

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class GUI:
    def __init__(self, difficulty='easy', board_size=8, square_size=60):
        self.board_size = board_size
        self.square_size = square_size
        self.game_controller = GameController(difficulty)
        self.board_width = self.board_size * self.square_size
        self.board_height = self.board_size * self.square_size
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.init_pygame()
        self.run_game()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Othello')
        self.font = pygame.font.Font(None, 36)
        self.difficulty = None  # Stores the selected difficulty
        self.current_player = BLACK

    def run_game(self):
        self.show_difficulty_selection()
        while True:
            self.check_events()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)

    def show_difficulty_selection(self):
        difficulty_selected = False
        while not difficulty_selected:
            self.screen.fill((0, 144, 103))  # Green background
            self.draw_text("Select Difficulty:", (self.board_width // 2, self.board_height // 4))
            self.draw_text("1. Easy", (self.board_width // 2, self.board_height // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board_width // 2 - 50 <= mouse_pos[0] <= self.board_width // 2 + 50:
                        if self.board_height // 2 <= mouse_pos[1] <= self.board_height // 2 + 30:
                            self.difficulty = 'easy'
                            difficulty_selected = True

    def draw_text(self, text, pos):
        text_surface = self.font.render(text, True, (255, 255, 255))
        rect = text_surface.get_rect()
        rect.center = pos
        self.screen.blit(text_surface, rect)

    def draw_board(self):
        self.screen.fill((0, 144, 103))  # Green background
        self.draw_grid()
        self.draw_pieces()
        if self.current_player == WHITE:  # Computer's turn
            self.make_computer_move()

        # Draw valid move indicators for the current player (BLACK)
        if self.current_player == BLACK:
            valid_moves = self.board.get_valid_moves(BLACK)
            for move in valid_moves:
                x, y = move[1] * self.square_size + self.square_size // 2, move[
                    0] * self.square_size + self.square_size // 2
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), self.square_size // 6)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.current_player == BLACK:  # User's turn only
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // self.square_size
                    col = mouse_pos[0] // self.square_size
                    if 0 <= row < self.board_size and 0 <= col < self.board_size:
                        if self.board.is_valid_move(row, col, self.current_player):
                            self.board.make_move(row, col, self.current_player)
                            self.current_player = WHITE  # Switch to computer's turn

    def draw_grid(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size
                y = row * self.square_size
                pygame.draw.rect(self.screen, (19, 26, 24), (x, y, self.square_size, self.square_size), 2)

    def draw_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                if self.board.board[row][col] == BLACK:
                    pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.square_size // 3)
                elif self.board.board[row][col] == WHITE:
                    pygame.draw.circle(self.screen, (255, 255, 255), (x, y), self.square_size // 3)

    def make_computer_move(self):
        if self.difficulty == 'easy':
            # Simple random move for easy difficulty
            valid_moves = self.board.get_valid_moves(WHITE)
            if valid_moves:
                row, col = random.choice(valid_moves)
                self.board.make_move(row, col, WHITE)
                self.current_player = BLACK  # Switch back to user's turn
