import chess

board = chess.Board()

while not (board.is_checkmate() or board.is_stalemate()):
    
