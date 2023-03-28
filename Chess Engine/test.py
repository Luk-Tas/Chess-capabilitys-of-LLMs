from ComEngineLLM import ComEngineLLM
import chess

board = chess.Board()
com = ComEngineLLM()
difficulty = "master"

move1 = chess.Move.from_uci("d2d3")
move2 = chess.Move.from_uci("g7g6")

board.push(move1)
board.push(move2)

print(com.engine_to_llm(board, difficulty))

next_move = "Ra1 Your turn: 2. b3 Nc6 A chess master would play the"

com.llm_to_engine(board, next_move)
print(board.move_stack)

