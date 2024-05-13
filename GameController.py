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


