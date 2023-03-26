import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\Lukas\Desktop\Ordner\Stockfish\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    print(result.move)

engine.quit()
