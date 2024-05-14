from Board import Board
from Player import Player

BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class GameController:
    def __init__(self, human_player, ai_player):
        self.human_player = human_player
        self.ai_player = ai_player
        self.current_player = human_player
        self.board = Board()  # Assuming you have a Board class to manage the game state

    def is_computer_turn(self):
        return self.current_player == self.ai_player

    def switch_turn(self):
        if self.current_player == self.human_player:
            self.current_player = self.ai_player
        else:
            self.current_player = self.human_player


