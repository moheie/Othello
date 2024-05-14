import pygame
import sys
from pygame.locals import *
import random

from AI import AIPlayer
from Board import Board
from GameController import GameController
from Player import Player

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class GUI:
    def __init__(self):
        self.SCREEN_SIZE = (640, 750)
        self.board_size = 8
        self.square_size = 80
        self.board_width = self.board_size * self.square_size
        self.board_height = self.board_size * self.square_size
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_player = None # Initialize player color choice
        self.difficulty = None  # Initialize difficulty choice
        self.init_pygame()
        self.background_image = pygame.image.load('desktop-wallpaper-engaging-blank-blank-blue-gaming.jpg')
        self.background_image = pygame.transform.scale(self.background_image, self.SCREEN_SIZE)
        pygame.display.set_caption('Othello')
        self.font = pygame.font.Font("foxonthego.ttf", 36)
        self.start_button_clicked = False
        self.run_game()

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Othello')

    def run_game(self):
        self.show_menu()
        self.start_time = pygame.time.get_ticks()

        self.game_controller = GameController(Player(self.current_player),
                                              AIPlayer(WHITE if self.current_player == BLACK else BLACK,
                                                       self.difficulty))
        while True:
            self.check_events()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(30)
            if self.board.is_game_over():
                self.declare_winner()
                break

    def animate_flip(self, row, col, color):
        for i in range(1, 11):
            # Adjust the color based on the player's color choice
            circle_color = (i * 25 if color == BLACK else 255 - i * 25, i * 25 if color == BLACK else 255 - i * 25,
                            i * 25 if color == BLACK else 255 - i * 25)
            pygame.draw.circle(self.screen, circle_color, (
            col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2),
                               self.square_size // 3)
            pygame.display.flip()
            pygame.time.wait(50)

    def declare_winner(self):
        # print on the screen
        black_count = sum(row.count(BLACK) for row in self.board.board)
        white_count = sum(row.count(WHITE) for row in self.board.board)
        if black_count > white_count:
            text = "Black Wins!"
        elif white_count > black_count:
            text = "White Wins!"
        else:
            text = "It's a tie!"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.board_width // 2, self.board_height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def show_menu(self):
        color_selected = False
        difficulty_selected = False
        start_button_clicked = False

        while not start_button_clicked:
            self.screen.fill((173, 216, 230))
            self.screen.blit(self.background_image, (0, 0))
            self.button(0, -200, "Othello")
            self.button(0, -150, "Select color")
            self.button(0, -100, "1. Black")
            self.button(0, -50, "2. White")
            self.button(0, 0, "Select Difficulty")
            self.button(0, 50, "1. Easy")
            self.button(0, 100, "2. Medium")
            self.button(0, 150, "3. Hard")
            self.button(0, 250, "Start")  # Add a Start button
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.board_height // 2 - 100 <= mouse_pos[1] <= self.board_height // 2 - 70:
                        self.current_player = BLACK
                        color_selected = True
                    elif self.board_height // 2 - 50 <= mouse_pos[1] <= self.board_height // 2 - 20:
                        self.current_player = WHITE
                        color_selected = True

                    if self.board_height // 2 <= mouse_pos[1] <= self.board_height // 2 + 50:
                        self.difficulty = 'easy'
                        difficulty_selected = True
                    elif self.board_height // 2 + 70 <= mouse_pos[1] <= self.board_height // 2 + 120:
                        self.difficulty = 'medium'
                        difficulty_selected = True
                    elif self.board_height // 2 + 140 <= mouse_pos[1] <= self.board_height // 2 + 190:
                        self.difficulty = 'hard'
                        difficulty_selected = True

                    if self.board_height // 2 + 210 <= mouse_pos[1] <= self.board_height // 2 + 260 and \
                            color_selected and difficulty_selected:  # Only start the game if color and difficulty are selected
                            start_button_clicked = True

    def button(self, x_offset, y_offset, text):
        font = pygame.font.Font("foxonthego.ttf", 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.board_width // 2 + x_offset, self.board_height // 2 + y_offset)
        mouse_pos = pygame.mouse.get_pos()

        # Define colors for highlighting and normal state
        normal_color = (173, 216, 230)
        hover_color = (0, 255, 0)  # Green color for highlighting

        # Check if the button text is "Start" or part of color/difficulty selection
        if text == "Start":
            target_rect = pygame.Rect(text_rect)  # Create a rect to draw the button
            if target_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, hover_color, target_rect)  # Highlight when hovered
            else:
                pygame.draw.rect(self.screen, normal_color, target_rect)  # Normal state

            self.screen.blit(text_surface, text_rect)
        else:
            # Draw colored square around selected color/difficulty
            if text == "1. Black" and self.current_player == BLACK :
                pygame.draw.rect(self.screen, (255, 0, 0), text_rect, 2)  # Red border for selected color
            elif text == "2. White" and self.current_player == WHITE :
                pygame.draw.rect(self.screen, (255, 0, 0), text_rect, 2)  # Red border for selected color
            elif text in ["1. Easy", "2. Medium", "3. Hard"] and self.difficulty == text.split(". ")[1].lower() :
                pygame.draw.rect(self.screen, (255, 0, 0), text_rect, 2)  # Red border for selected difficulty
            else:
                pygame.draw.rect(self.screen, normal_color, text_rect)  # Normal state for other options

            self.screen.blit(text_surface, text_rect)

    def showScore(self):
        black_count = sum(row.count(BLACK) for row in self.board.board)
        white_count = sum(row.count(WHITE) for row in self.board.board)
        text = "Black: " + str(black_count) + "         " + " White: " + str(white_count)
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.board_width // 2, self.board_height + 70))
        self.screen.blit(text_surface, text_rect)

    def draw_current_player_indicator(self):
        text = "Current Player: " + self.current_player
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.board_width // 2 +150, self.board_height + 30))
        self.screen.blit(text_surface, text_rect)

    def draw_valid_moves(self):
        valid_moves = self.board.get_valid_moves(self.current_player)
        for move in valid_moves:
            x, y = move[1] * self.square_size + self.square_size // 2, move[0] * self.square_size + self.square_size // 2
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), self.square_size // 6)

    def draw_board(self):
        self.screen.fill((173, 216, 230))
        self.screen.blit(self.background_image, (0, 0))
        self.draw_grid()
        self.draw_pieces()
        self.draw_current_player_indicator()
        self.draw_valid_moves()
        self.showScore()
        self.show_timer()  # Show the timer

        # Check if it's the computer's turn based on the player's color choice
        if self.current_player == WHITE and self.current_player != BLACK:
            self.make_computer_move()



    def show_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"Time: {minutes}:{seconds:02d}"
        text_surface = self.font.render(timer_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.board_width // 2 - 200, self.board_height +30 ))  # Adjust the position as needed
        self.screen.blit(text_surface, text_rect)

    def draw_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board.board[row][col] == BLACK:
                    pygame.draw.circle(self.screen, (0, 0, 0), (
                    col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2),
                                       self.square_size // 3)
                elif self.board.board[row][col] == WHITE:
                    pygame.draw.circle(self.screen, (255, 255, 255), (
                    col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2),
                                       self.square_size // 3)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // self.square_size
                col = mouse_pos[0] // self.square_size

                if self.current_player == BLACK or self.current_player == WHITE:  # Player's turn only
                    player_color = self.current_player
                    if 0 <= row < self.board_size and 0 <= col < self.board_size:
                        if self.board.is_valid_move(row, col, player_color):
                            self.animate_flip(row, col, player_color)
                            self.board.make_move(row, col, player_color)
                            self.current_player = WHITE if player_color == BLACK else BLACK  # Switch player's turn

                def check_events(self):
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if self.start_button_clicked:  # Check if the game has started
                                row = mouse_pos[1] // self.square_size
                                col = mouse_pos[0] // self.square_size

                                if self.current_player == BLACK or self.current_player == WHITE:  # Player's turn only
                                    player_color = self.current_player
                                    if 0 <= row < self.board_size and 0 <= col < self.board_size:
                                        if self.board.is_valid_move(row, col, player_color):
                                            self.animate_flip(row, col, player_color)
                                            self.board.make_move(row, col, player_color)
                                            self.current_player = WHITE if player_color == BLACK else BLACK  # Switch player's turn
                            else:
                                self.show_menu()  # If the game has not started, show the menu
                # Uncomment this block if you want to manually trigger the computer's move
                # if self.current_player == WHITE:  # Computer's turn
                #     self.make_computer_move()

    def draw_grid(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size
                y = row * self.square_size
                pygame.draw.rect(self.screen, (19, 26, 24), (x, y, self.square_size, self.square_size), 2)

    def make_computer_move(self):
        computer_color = WHITE if self.current_player == BLACK else BLACK  # Get computer's color based on player's choice

        if self.current_player == computer_color:  # Computer's turn only
            if self.difficulty == 'easy':
                depth = 1
            elif self.difficulty == 'medium':
                depth = 3
            elif self.difficulty == 'hard':
                depth = 5

            ai_player = AIPlayer(computer_color, depth)  # Use computer's color for AIPlayer
            ai_player.make_move(self.board)
            self.current_player = BLACK if computer_color == WHITE else WHITE  # Switch back to user's turn


