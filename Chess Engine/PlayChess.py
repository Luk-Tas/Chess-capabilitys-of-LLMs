import random
import chess
from ChessEngine import ChessEngine
from ComEngineLLM import ComEngineLLM

# Enter your stockfish path
engine = ChessEngine\
    (r"C:\Users\Lukas\Desktop\Ordner\Stockfish\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

# Enter difficulty level
difficulty = "beginner"

board = chess.Board()
com = ComEngineLLM()

engine_wins = 0
llm_wins = 0
draws = 0
increment = 1
white_wins = '1-0'
black_wins = '0-1'
draw = '1/2-1/2'


engine.change_difficulty(difficulty)

# select who starts
engine_start = True
#engine_start = bool(random.getrandbits(1))

if engine_start:
    while not board.is_game_over():
        old_move_stack = board.move_stack
        result = engine.get_best_move(board.fen())
        print(result)
        move = chess.Move.from_uci(result)
        board.push(move)
        for x in range(0, 9):
            try:
                print(x)
                print(com.engine_to_llm(board, difficulty))
                llm_answer = input()
                board = com.llm_to_engine(board, llm_answer)
                print(board.move_stack)
                break
            except chess.InvalidMoveError:
                print("phase 2 wrong")
                pass
        if old_move_stack == board.move_stack:
            engine_wins = engine_wins + increment
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
        for x in range(0, 9):
            try:
                print(com.engine_to_llm(board, difficulty))
                llm_answer = input()
                board = com.llm_to_engine(board, llm_answer)
                print(board.move_stack)
                break
            except chess.InvalidMoveError:
                pass
        if old_move_stack == board.move_stack:
            engine_wins = engine_wins + increment
            break
        old_move_stack = board.move_stack
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
