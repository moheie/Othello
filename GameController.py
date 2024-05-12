from Board import Board
from Player import Player

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class GameController:
    def __init__(self, difficulty):
        self.board = Board()
        self.black_player = Player(BLACK)
        self.white_player = Player(WHITE)
        self.current_player = self.black_player if difficulty == 'easy' else self.white_player

    def switch_player(self):
        self.current_player = self.white_player if self.current_player == self.black_player else self.black_player

    def play_game(self):
        # Main game loop to manage turns and game flow
        while not self.board.is_game_over():
            self.board.display_board()
            print(f"\n{self.current_player.color} player's turn.")
            self.current_player.make_move(self.board)
            self.switch_player()
        self.board.display_board()
        self.declare_winner()

    def declare_winner(self):
        # Determine and print the winner based on the number of pieces
        pass  # Add your implementation here