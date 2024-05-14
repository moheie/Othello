from Player import Player
BLACK = 'B'
WHITE = 'W'
EMPTY = ' '

class AIPlayer(Player):

    def __str__(self):
        return self.color
    def __init__(self, color, difficulty):
        super().__init__(color)
        self.difficulty = difficulty

    def make_move(self, board):
        _, move = self.alpha_beta_search(board, self.difficulty)
        if move:
            board.make_move(*move, self.color)


    def utility(self, board):
        black_count, white_count = board.count_pieces()
        return black_count - white_count if self.color == BLACK else white_count - black_count


    def alpha_beta_search(self, board, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0 or board.is_game_over() or not board.get_valid_moves(self.color):
            return self.utility(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in board.get_valid_moves(self.color):
                new_board = board.copy()
                new_board.make_move(*move, self.color)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval and move is not None:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha or best_move is None:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in board.get_valid_moves(BLACK if self.color == WHITE else WHITE):
                new_board = board.copy()
                new_board.make_move(*move, BLACK if self.color == WHITE else WHITE)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval and move is not None:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha or best_move is None:
                    break
            return min_eval, best_move

    # def heuristic(self, board):
    #     black_count, white_count = board.count_pieces()
    #     # A simple heuristic considering piece count difference
    #     return black_count - white_count if self.color == BLACK else white_count - black_count
