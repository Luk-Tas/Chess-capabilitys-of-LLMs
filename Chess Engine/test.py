from ComEngineLLM import ComEngineLLM
from BloomZ_API import AccessBloomZAPI
import chess
import re

board = chess.Board()
com = ComEngineLLM()
difficulty = "master"

move1 = chess.Move.from_uci("d2d3")
move2 = chess.Move.from_uci("g7g6")
move3 = chess.Move.from_uci("a2a4")
next_move = "a5"

board.push(move1)
board.push(move2)
# board.push(move3)

# print(round(len(board.move_stack)/2))

# print(com.engine_to_llm_style1(board, difficulty))

"""
next_move = "e4 Your turn: 2. b3 Nc6 A chess master would play the"

com.llm_to_engine(board, next_move)
print(board.move_stack)
"""

BloomZAPI = AccessBloomZAPI()
prompt = com.engine_to_llm_prob(board, difficulty, next_move)
print(prompt)
completion = BloomZAPI.create_prob(prompt)
# print(completion)
tuple_list = com.extract_token_data(str(completion))
print(tuple_list)
string = ' a4'

result = com.calculate_prob_sum_str(string, tuple_list)
print(result)


# board = com.llm_to_engine(board, prompt, completion)
# print(board.move_stack)




