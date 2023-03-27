from stockfish import Stockfish

class ChessEngine:

    chess_level = ["Beginner", "KIT_Professor"]

    def __init__(self, engine_path):
        self.stockfish = Stockfish(engine_path)

    def change_difficulty(self, chess_level):
        if chess_level == self.chess_level[0]:
            self.stockfish.update_engine_parameters({"Skill Level": 1})
        if chess_level == self.chess_level[1]:
            self.stockfish.update_engine_parameters({"Skill Level": 13})

    def get_best_move(self, board):
        self.stockfish.set_fen_position(board)
        return self.stockfish.get_best_move()
