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
        self.start_button_clicked = False
        self.run_game()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Othello')
        self.font = pygame.font.Font(None, 36)
        self.difficulty = None  # Stores the selected difficulty
        self.current_player = BLACK

    def run_game(self):
        self.draw_start_button()
        pygame.display.flip()
        while not self.start_button_clicked:
            self.check_events()
        self.show_difficulty_selection()
        while True:
            self.check_events()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)
            if self.board.is_game_over():
                self.declare_winner()
                break

    def draw_start_button(self):
        self.screen.fill((173, 216, 230))
        self.button("Start", self.board_width // 2, self.board_height // 2)

    def button(self, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        pygame.draw.rect(self.screen, (255, 255, 255), (text_rect.left - 20, text_rect.top - 20, text_rect.width + 40,
                                                        text_rect.height + 40))
        self.screen.blit(text_surface, text_rect)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.board_width // 2 - self.square_size // 2 <= mouse_pos[
                    0] <= self.board_width // 2 + self.square_size // 2:
                    if self.board_height // 2 - self.square_size // 2 <= mouse_pos[
                        1] <= self.board_height // 2 + self.square_size // 2:
                        self.start_button_clicked = True

    def show_difficulty_selection(self):
        difficulty_selected = False
        while not difficulty_selected:
            self.screen.fill((173, 216, 230))
            self.button("Select Difficulty", self.board_width // 2, self.board_height // 2 - 50)
            self.button("1. Easy", self.board_width // 2, self.board_height // 2)
            self.button("2. Medium", self.board_width // 2, self.board_height // 2 + 50)
            self.button("3. Hard", self.board_width // 2, self.board_height // 2 + 100)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board_width // 2 - self.square_size // 2 <= mouse_pos[
                        0] <= self.board_width // 2 + self.square_size // 2:
                        if self.board_height // 2 - 50 - self.square_size // 2 <= mouse_pos[
                            1] <= self.board_height // 2 - 50 + self.square_size // 2:
                            self.difficulty = 'easy'
                            difficulty_selected = True
                        elif self.board_height // 2 - self.square_size // 2 <= mouse_pos[
                            1] <= self.board_height // 2 + self.square_size // 2:
                            self.difficulty = 'medium'
                            difficulty_selected = True
                        elif self.board_height // 2 + 50 - self.square_size // 2 <= mouse_pos[
                            1] <= self.board_height // 2 + 50 + self.square_size // 2:
                            self.difficulty = 'hard'
                            difficulty_selected = True
    def declare_winner(self):
        black_count = sum(row.count(BLACK) for row in self.board.board)
        white_count = sum(row.count(WHITE) for row in self.board.board)
        if black_count > white_count:
            print("Black wins!")
        elif white_count > black_count:
            print("White wins!")
        else:
            print("It's a draw!")

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
        elif self.difficulty == 'medium':
            # Implement medium difficulty logic here
            pass
        elif self.difficulty == 'hard':
            # Implement hard difficulty logic here
            pass


