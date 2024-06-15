from enum import Enum
from typing import Self

class Color(Enum):
    BLACK = 0
    WHITE = 1

    def opposite(self) -> Self:
        if self == Color.BLACK:
            return Color.WHITE
        else:
            return Color.BLACK
    
    def to_state(self):
        if self == Color.BLACK:
            return CellState.BLACK
        elif self == Color.WHITE:
            return CellState.WHITE

class Difficulty(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'

class CellState(Enum):
    UNOCCUPIED = 0
    BLACK = 1
    WHITE = 2

    def opposite(self) -> Self:
        if self == CellState.BLACK:
            return CellState.WHITE
        elif self == CellState.WHITE:
            return CellState.BLACK
        else:
            raise RuntimeError('Cannot determine the opposite of an unoccupied cell')

    def to_color(self) -> Color:
        if self == CellState.BLACK:
            return Color.BLACK
        elif self == CellState.WHITE:
            return Color.WHITE
        else:
            raise RuntimeError('Cannot convert an unoccupied cell state into a color')