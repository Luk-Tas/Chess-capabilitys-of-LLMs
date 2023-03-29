import copy
import random
import chess
from ChessEngine import ChessEngine
from ComEngineLLM import ComEngineLLM
from BloomZ_API import AccessBloomZAPI

# Enter your stockfish path
engine = ChessEngine\
    (r"C:\Users\Lukas\Desktop\Dokumente\Stockfish\stockfish_15.1_win_x64_avx2\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

# Enter difficulty level, choose from "beginner" and "master"
difficulty = "master"

board = chess.Board()
com = ComEngineLLM()
bloomZ = AccessBloomZAPI()

engine_wins = 0
engine_wins_by_wrong_move = 0
llm_wins = 0
draws = 0
increment = 1
white_wins = '1-0'
black_wins = '0-1'
draw = '1/2-1/2'


engine.change_difficulty(difficulty)

# select who starts
# engine_start = True
engine_start = bool(random.getrandbits(1))
for index in range(0,10):
    if engine_start:
        while not board.is_game_over():
            # print(old_move_stack)
            result = engine.get_best_move(board.fen())
            # print(result)
            move = chess.Move.from_uci(result)
            board.push(move)
            old_move_stack = copy.copy(board.move_stack)
            for x in range(0, 3):
                try:
                    print(com.engine_to_llm(board, difficulty))
                    prompt = com.engine_to_llm(board, difficulty)
                    llm_answer = bloomZ.create_completion(prompt)
                    board = com.llm_to_engine(board, prompt, llm_answer)
                    break
                except chess.InvalidMoveError:
                    pass
            if old_move_stack == board.move_stack:
                engine_wins = engine_wins + increment
                engine_wins_by_wrong_move = engine_wins_by_wrong_move + increment
                break
        if board.is_game_over():
            if board.outcome().result() == white_wins:
                engine_wins = engine_wins + increment
            elif board.outcome().result() == black_wins:
                llm_wins = llm_wins + increment
            elif board.outcome().result() == draw:
                draws = draws + increment
    else:
        while not board.is_game_over():
            old_move_stack = copy.copy(board.move_stack)
            for x in range(0, 3):
                try:
                    print(x)
                    print(com.engine_to_llm(board, difficulty))
                    prompt = com.engine_to_llm(board, difficulty)
                    llm_answer = bloomZ.create_completion(prompt)
                    board = com.llm_to_engine(board, prompt, llm_answer)
                    break
                except chess.InvalidMoveError:
                    pass
            if old_move_stack == board.move_stack:
                engine_wins = engine_wins + increment
                engine_wins_by_wrong_move = engine_wins_by_wrong_move + increment
                break
            result = engine.get_best_move(board.fen())
            print(result)
            move = chess.Move.from_uci(result)
            board.push(move)
        if board.is_game_over():
            if board.outcome().result() == black_wins:
                engine_wins = engine_wins + increment
            elif board.outcome().result() == white_wins:
                llm_wins = llm_wins + increment
            elif board.outcome().result() == draw:
                draws = draws + increment

print("engine_wins: " + str(engine_wins) + ", ", "engine_wins_by_wrong_move: " + str(engine_wins_by_wrong_move)
      + ", ", "llm_wins: " + str(llm_wins) + ", ", "draws: " + str(draws))
