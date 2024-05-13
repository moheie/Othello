from Player import Player
BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class AIPlayer(Player):
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.difficulty = difficulty

    def make_move(self, board):
        _, move = self.alpha_beta_search(board, self.difficulty)
        if move:
            board.make_move(*move, self.color)

    def minimax(self, board, depth, maximizing_player=True):
        if depth == 0 or board.is_game_over():
            return self.utility(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in board.get_valid_moves(self.color):
                new_board = board.copy()
                new_board.make_move(*move, self.color)
                eval, _ = self.minimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in board.get_valid_moves(BLACK if self.color == WHITE else WHITE):
                new_board = board.copy()
                new_board.make_move(*move, BLACK if self.color == WHITE else WHITE)
                eval, _ = self.minimax(new_board, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def utility(self, board):
        black_count, white_count = board.count_pieces()
        return black_count - white_count if self.color == BLACK else white_count - black_count


    def alpha_beta_search(self, board, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0 or board.is_game_over():
            return self.utility(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in board.get_valid_moves(self.color):
                new_board = board.copy()
                new_board.make_move(*move, self.color)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in board.get_valid_moves(BLACK if self.color == WHITE else WHITE):
                new_board = board.copy()
                new_board.make_move(*move, BLACK if self.color == WHITE else WHITE)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def heuristic(self, board):
        # Implement a heuristic function to evaluate the board state
        pass