import chess
from ChessEngine import ChessEngine

engine = ChessEngine\
    (r"C:\Users\Lukas\Desktop\Ordner\Stockfish\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
board = chess.Board()

print(engine.stockfish.get_parameters())
engine.change_difficulty("Beginner")
print(engine.stockfish.get_parameters())
engine.change_difficulty("KIT_Professor")
print(engine.stockfish.get_parameters())

while not board.is_game_over():
    engine.change_difficulty("Beginner")
    result = engine.get_best_move(board.fen())
    print(result)
    move = chess.Move.from_uci(result)
    board.push(move)
    #print(engine.stockfish.get_parameters())
    engine.change_difficulty("KIT_Professor")
    result = engine.get_best_move(board.fen())
    print(result)
    move = chess.Move.from_uci(result)
    board.push(move)
    #print(engine.stockfish.get_parameters())


print(board.outcome().result())

