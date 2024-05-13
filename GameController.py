from Board import Board
from Player import Player

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class GameController:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1



