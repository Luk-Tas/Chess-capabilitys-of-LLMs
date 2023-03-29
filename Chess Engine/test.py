from ComEngineLLM import ComEngineLLM
from BloomZ_API import AccessBloomZAPI
import chess

board = chess.Board()
com = ComEngineLLM()
difficulty = "master"

move1 = chess.Move.from_uci("d2d3")
move2 = chess.Move.from_uci("g7g6")
move3 = chess.Move.from_uci("a2a4")

board.push(move1)
board.push(move2)
board.push(move3)

print(round(len(board.move_stack)/2))

print(com.engine_to_llm_style1(board, difficulty))

"""
next_move = "e4 Your turn: 2. b3 Nc6 A chess master would play the"

com.llm_to_engine(board, next_move)
print(board.move_stack)
"""

BloomZAPI = AccessBloomZAPI()
prompt = com.engine_to_llm_style1(board, difficulty)
completion = BloomZAPI.create_completion(prompt)
print(completion)

board = com.llm_to_engine(board, prompt, completion)
print(board.move_stack)




