import copy
import random
import chess
from ChessEngine import ChessEngine
from ComEngineLLM import ComEngineLLM
from BloomZ_API import AccessBloomZAPI

# Enter your stockfish path
engine = ChessEngine\
    (r"C:\Users\Lukas\Desktop\Ordner\Stockfish\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")

# Enter difficulty level, choose from "beginner" and "master"
difficulty = "beginner"

engine_wins = 0
engine_wins_by_wrong_move = 0
llm_wins = 0
draws = 0
increment = 1
white_wins = '1-0'
black_wins = '0-1'
draw = '1/2-1/2'
sum_moves_played = 0
EXPERIMENT_RUNS = 10
experiment_summery = []


engine.change_difficulty(difficulty)

# select who starts
# engine_start = True
engine_start = bool(random.getrandbits(1))
for index in range(0, EXPERIMENT_RUNS):

    board = chess.Board()
    com = ComEngineLLM()
    bloomZ = AccessBloomZAPI()

    if engine_start:
        while not board.is_game_over():
            # print(old_move_stack)
            result = engine.get_best_move(board.fen())
            print(result)
            move = chess.Move.from_uci(result)
            board.push(move)
            old_move_stack = copy.copy(board.move_stack)
            for x in range(0, 3):
                try:
                    legal_moves_list = com.get_legal_moves_list(board)
                    # print(legal_moves_list)
                    possible_moves = []
                    for move in legal_moves_list:
                        move_token = " " + move
                        # print(move_token)
                        prompt = com.engine_to_llm_prob(board, difficulty, move_token)
                        # print(prompt)
                        llm_answer = bloomZ.create_prob(prompt)
                        answer_token_list = com.extract_token_data(str(llm_answer))
                        # print(answer_token_list)
                        possible_moves.append(com.calculate_prob_sum_str(move_token, answer_token_list))
                    highest_value_move = max(possible_moves, key=lambda x: x[1])
                    # print(highest_value_move)
                    next_move = str(highest_value_move[0]).lstrip()
                    print(next_move)
                    board.push_san(next_move)
                    break
                except chess.InvalidMoveError:
                    pass
                except ValueError:
                    pass
            if (old_move_stack == board.move_stack) & (not board.is_game_over()):
                engine_wins = engine_wins + increment
                engine_wins_by_wrong_move = engine_wins_by_wrong_move + increment
                break
        if board.is_game_over():
            if board.outcome().result() == white_wins:
                print("engine wins")
                engine_wins = engine_wins + increment
            elif board.outcome().result() == black_wins:
                print("llm wins")
                llm_wins = llm_wins + increment
            elif board.outcome().result() == draw:
                print("draw")
                draws = draws + increment
    else:
        while not board.is_game_over():
            old_move_stack = copy.copy(board.move_stack)
            for x in range(0, 3):
                try:
                    legal_moves_list = com.get_legal_moves_list(board)
                    # print(legal_moves_list)
                    possible_moves = []
                    for move in legal_moves_list:
                        move_token = " " + move
                        # print(move_token)
                        prompt = com.engine_to_llm_prob(board, difficulty, move_token)
                        # print(prompt)
                        llm_answer = bloomZ.create_prob(prompt)
                        answer_token_list = com.extract_token_data(str(llm_answer))
                        # print(answer_token_list)
                        possible_moves.append(com.calculate_prob_sum_str(move_token, answer_token_list))
                    highest_value_move = max(possible_moves, key=lambda x: x[1])
                    # print(highest_value_move)
                    next_move = str(highest_value_move[0]).lstrip()
                    # print(next_move)
                    board.push_san(next_move)
                    break
                except chess.InvalidMoveError:
                    pass
                except ValueError:
                    pass
            if (old_move_stack == board.move_stack) & (not board.is_game_over()):
                engine_wins = engine_wins + increment
                engine_wins_by_wrong_move = engine_wins_by_wrong_move + increment
                break
            result = engine.get_best_move(board.fen())
            move = chess.Move.from_uci(result)
            board.push(move)
        if board.is_game_over():
            if board.outcome().result() == black_wins:
                print("engine wins")
                engine_wins = engine_wins + increment
            elif board.outcome().result() == white_wins:
                print("llm wins")
                llm_wins = llm_wins + increment
            elif board.outcome().result() == draw:
                print("draw")
                draws = draws + increment
    experiment_summery.append(len(board.move_stack))
    print("game no: " + str(index) + " is done.")
    #sum_moves_played = sum_moves_played + round(len(board.move_stack)/2)

# average_played_moves = sum_moves_played/EXPERIMENT_RUNS

print("engine_wins: " + str(engine_wins) + ", ", "engine_wins_by_wrong_move: " + str(engine_wins_by_wrong_move)
      + ", ", "llm_wins: " + str(llm_wins) + ", ", "draws: " + str(draws))

print(experiment_summery)
