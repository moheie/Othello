"""
todo:
    1. why is evaluation still infinity
    2. factor being unable to play into the evaluation
"""

from copy import deepcopy
from threading import Timer
from typing import Self
import sys

from game.state import CellState, Difficulty, Color
from game.stepper import DirectionStepper, LeftStepper, RightStepper, UpStepper, DownStepper

DEFAULT_ROW_COUNT = 8
DEFAULT_COLUMN_COUNT = 8

DIFFICULTY_MAX_DEPTHS: dict[Difficulty, int] = {
    Difficulty.EASY: 3,
    Difficulty.MEDIUM: 5,
    Difficulty.HARD: 7,
}

DIFFICULTY_FAKE_LAG: dict[Difficulty, int] = {
    Difficulty.EASY: 1,
    Difficulty.MEDIUM: 1,
    Difficulty.HARD: 1,
}

NEGATIVE_INF = -sys.maxsize - 1
INF = sys.maxsize

class Action:
    def __init__(self, position) -> None:
        pass

class Game:
    def __init__(self, selected_color: Color, difficulty: Difficulty, rows: int = DEFAULT_ROW_COUNT, columns: int = DEFAULT_COLUMN_COUNT) -> None:
        self.board: list[list[CellState]] = []

        for i in range(rows):
            row = []

            for j in range(columns):
                row.append(CellState.UNOCCUPIED)

            self.board.append(row)
        
        # Not sure how this will behave with odd numbers
        self.board[rows // 2 - 1][columns // 2 - 1] = CellState.WHITE
        self.board[rows // 2 - 1][columns // 2] = CellState.BLACK

        self.board[rows // 2][columns // 2 - 1] = CellState.BLACK
        self.board[rows // 2][columns // 2] = CellState.WHITE

        # A pool of placed pieces to optimize the process of calculating available moves
        self.pieces: dict[Color, set[tuple[int, int]]] = {
            Color.BLACK: {
                (rows // 2 - 1, columns // 2),
                (rows // 2, columns // 2 - 1),
            },
            Color.WHITE: {
                (rows // 2 - 1, columns // 2 - 1),
                (rows // 2, columns // 2),
            },
        }

        self.last_placed_piece: tuple[int, int] = None

        """ self.board = [
            [CellState.UNOCCUPIED, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.UNOCCUPIED, CellState.UNOCCUPIED],
            [CellState.UNOCCUPIED, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.UNOCCUPIED],
            [CellState.WHITE, CellState.BLACK, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE],
            [CellState.WHITE, CellState.BLACK, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE],
            [CellState.UNOCCUPIED, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE],
            [CellState.UNOCCUPIED, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE, CellState.WHITE],
            [CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.WHITE, CellState.WHITE, CellState.BLACK, CellState.WHITE],
            [CellState.UNOCCUPIED, CellState.UNOCCUPIED, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.BLACK, CellState.UNOCCUPIED],
        ]

        self.pieces = self.find_all_pieces() """
        
        self.rows = rows
        self.columns = columns
        self.max_disks = rows * columns
        
        self.steppers: dict[str, DirectionStepper] = {
            'left': LeftStepper(rows, columns),
            'right': RightStepper(rows, columns),
            'up': UpStepper(rows, columns),
            'down': DownStepper(rows, columns),
        }

        self.min_color = selected_color
        self.max_color = selected_color.opposite()
        self.difficulty = difficulty

        self.turn = Color.BLACK
        self.available_moves: set[tuple[int, int]] = self.find_available_moves()

        self.start_turn()

    def is_min_turn(self):
        return self.turn == self.min_color

    def is_max_turn(self):
        return not self.is_min_turn()
    
    def is_player_turn(self):
        return self.is_min_turn()
    
    def get_cell(self, position: tuple[int, int]) -> CellState:
        row = position[0]
        column = position[1]

        return self.board[row][column]
    
    def get_available_neighbors(self, position: tuple[int, int], state: CellState, limit = INF):
        neighbors = set()
        count = 0

        for stepper in self.steppers.values():
            if stepper.check_pre_condition(position):
                new_position = stepper.step(position)

                if self.get_cell(new_position) == CellState.UNOCCUPIED and self.will_cell_outflank(new_position, state):
                    count += 1
                    neighbors.add(new_position)

                    if count >= limit:
                        break
        
        return neighbors

    
    def find_available_moves(self, color: Color = None, limit = INF):
        if color == None:
            color = self.turn

        opponent_pieces = self.pieces[color.opposite()]
        available_moves = set()
        count = 0

        for position in opponent_pieces:
            neighbors = self.get_available_neighbors(position, color.to_state(), limit - count)
            count += len(neighbors)

            available_moves.update(neighbors)

            if count >= limit:
                break
        
        return available_moves
    
    def find_outflanked_cells(
        self,
        position: tuple[int, int],
        state: CellState,
        stepper: DirectionStepper
    ) -> set[tuple[int, int]]:
        if state == None:
            state = self.get_cell(position)
        
        opponent_state = state.opposite()

        curr_position = stepper.step(position)
        curr_state: CellState = None

        cells = set()

        while stepper.check_condition(curr_position):
            curr_state = self.get_cell(curr_position)

            if curr_state == opponent_state:
                cells.add(curr_position)

                curr_position = stepper.step(curr_position)
            else:
                break
        
        # If final state is not the same as the initial state (same color), clear outflanked cells
        if curr_state != state:
            cells.clear()
        
        return cells


    def get_outflanked_cells(
        self,
        position: tuple[int, int],
        state: CellState = None,
        limit = INF
    ) -> set[tuple[int, int]]:
        cells = set()

        for stepper in self.steppers.values():
            cells.update(self.find_outflanked_cells(position, state, stepper))

            if len(cells) >= limit:
                break
        
        return cells
    
    def will_cell_outflank(self, position: tuple[int, int], state: CellState) -> bool:
        outflanked_cells = self.get_outflanked_cells(position, state, 1)

        return len(outflanked_cells) > 0
    
    def swap_cell_states(self, cells: set[tuple[int, int]]) -> None:
        for position in cells:
            curr_state = self.get_cell(position)
            curr_color = curr_state.to_color()
            
            opposite_state = curr_state.opposite()
            opposite_color = opposite_state.to_color()

            self.pieces[curr_color].remove(position)
            self.pieces[opposite_color].add(position)

            self.board[position[0]][position[1]] = opposite_state
    
    def find_all_pieces(self):
        pieces: dict[Color, set[tuple[int, int]]] = {
            Color.BLACK: set(),
            Color.WHITE: set(),
        }

        for row in range(self.rows):
            for column in range(self.columns):
                position = (row, column)
                state = self.get_cell(position)

                if state != CellState.UNOCCUPIED:
                    pieces[state.to_color()].add(position)
        
        return pieces

    def place_cell(self, position: tuple[int, int], is_simulated = False):
        row = position[0]
        column = position[1]

        if position in self.available_moves:
            self.pieces[self.turn].add(position)
            self.board[row][column] = self.turn.to_state()
            self.last_placed_piece = position

            # Check for outflanking
            outflanked_cells = self.get_outflanked_cells(position)
            
            self.swap_cell_states(outflanked_cells)
            
            self.turn = self.turn.opposite()
            self.available_moves = self.find_available_moves()

            if not is_simulated:
                self.start_turn()

    def skip_turn(self):
        self.turn = self.turn.opposite()
        self.available_moves = self.find_available_moves()

        self.start_turn()

    def start_turn(self):
        if self.is_over():
            return

        if len(self.available_moves) == 0:
            return self.skip_turn()

        if self.is_max_turn():
            self.start_max_turn()

    def start_max_turn(self):
        # Simulate lag so the player can see the AI's move being made
        delay = DIFFICULTY_FAKE_LAG[self.difficulty]
        
        timer = Timer(delay, self.play_max_turn)
        timer.start()

    def play_max_turn(self):
        print(self.difficulty, DIFFICULTY_MAX_DEPTHS[self.difficulty])
        action = minimax(self, DIFFICULTY_MAX_DEPTHS[self.difficulty], NEGATIVE_INF, INF)

        self.place_cell(action.position)

    def get_count(self, color: Color):
        return len(self.pieces[color])

    def is_over(self) -> bool:
        black_count = self.get_count(Color.BLACK)
        white_count = self.get_count(Color.WHITE)

        if black_count + white_count == self.max_disks:
            return True

        black_moves = self.find_available_moves(Color.BLACK, 1)
        white_moves = self.find_available_moves(Color.WHITE, 1)

        if not any(black_moves) and not any(white_moves):
            return True

        return False

    def get_max_score(self) -> int:
        return self.get_count(self.max_color) - self.get_count(self.min_color)

    def get_winner(self) -> Color:
        max_score = self.get_max_score()

        if max_score > 0:
            return self.max_color
        elif max_score < 0:
            return self.min_color
        else:
            return None

class Action:
    def __init__(self, position: tuple[int, int], evaluation: int) -> None:
        self.position = position
        self.evaluation = evaluation

    def __repr__(self) -> str:
        return f"<Action position={self.position} evaluation={self.evaluation}>"
    
    def __lt__(self, other: Self) -> bool:
        return self.evaluation < other.evaluation

    def __le__(self, other: Self) -> bool:
        return self.evaluation <= other.evaluation
    
    def __gt__(self, other: Self) -> bool:
        return self.evaluation > other.evaluation
    
    def __ge__(self, other: Self) -> bool:
        return self.evaluation >= other.evaluation

def minimax(game: Game, depth: int, alpha: int, beta: int) -> Action:
    if depth == 0 or game.is_over():
        return Action(None, game.get_max_score())

    if game.is_max_turn():
        max_action = Action(None, NEGATIVE_INF)

        for position in game.available_moves:
            hypothetical_game = deepcopy(game)
            hypothetical_game.place_cell(position, True)

            action: Action = minimax(hypothetical_game, depth - 1, alpha, beta)

            if action >= max_action:
                max_action = Action(position, action.evaluation)
            
            alpha = max(alpha, action.evaluation)
            
            if beta <= alpha:
                break

                    
        return max_action
    else:
        min_action = Action(None, INF)

        print(game.available_moves)

        for position in game.available_moves:
            hypothetical_game = deepcopy(game)
            hypothetical_game.place_cell(position, True)

            action: Action = minimax(hypothetical_game, depth - 1, alpha, beta)
            new_action = Action(position, action.evaluation)

            if action <= min_action:
                min_action = new_action
     
            beta = min(beta, action.evaluation)
            
            if beta <= alpha:
                break
        
        return min_action