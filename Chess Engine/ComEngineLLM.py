import copy

import chess
import re
import json


class ComEngineLLM:
    __STYLE1_PROMPT1 = "Chess Game: "
    __STYLE1_PROMPT2 = "\nA chess "
    __STYLE1_PROMPT3 = " would play the move:"
    __STYLE2_PROMPT1 = "The following is a chess game between two chess "
    __STYLE2_PROMPT2 = "s:\n"
    __STYLE3_PROMPT1 = "Legal moves:\n"
    __STYLE3_PROMPT2 = "The following is a chess game between two chess "
    __STYLE3_PROMPT3 = "s:\n"
    __PROMPT_PARAGRAPH = "\n"
    __MAX_SAN_LENGTH = 11
    __MIN_SAN_LENGTH = 1

    # currently unused
    __COUNT_DOWN_STEP = -1

    def engine_to_llm_style1(self, board: chess.Board, difficulty):
        # prompt = self.__STYLE1_PROMPT1
        temporary_board = chess.Board()
        move_list = temporary_board.variation_san(board.move_stack)
        prompt = self.__STYLE1_PROMPT1 + move_list + self.__STYLE1_PROMPT2 + difficulty + self.__STYLE1_PROMPT3
        return prompt

    def engine_to_llm_style2(self, board: chess.Board, difficulty):
        temporary_board = chess.Board()
        move_list = temporary_board.variation_san(board.move_stack)
        prompt = self.__STYLE2_PROMPT1 + difficulty + self.__STYLE2_PROMPT2 + move_list
        return prompt

    def engine_to_llm_prob(self, board: chess.Board, difficulty, next_move: str):
        prompt = ""
        legal_moves = self.__extract_legal_moves(board)
        # print(legal_moves)
        temporary_board = chess.Board()
        move_list = temporary_board.variation_san(board.move_stack)
        # prompt = self.__STYLE3_PROMPT1 + legal_moves
        prompt = prompt + self.__PROMPT_PARAGRAPH + self.__STYLE3_PROMPT2 + difficulty
        prompt = prompt + self.__STYLE3_PROMPT3 + move_list

        if len(board.move_stack) % 2 == 0:
            prompt = prompt + " " + str(int(len(board.move_stack)/2) + 1) + "." + next_move
        else:
            prompt = prompt + next_move

        return prompt

    def llm_to_engine(self, board: chess.Board, prompt: str, next_move: str):
        next_move = next_move.removeprefix(prompt)
        print(next_move)
        old_move_stack = copy.copy(board.move_stack)
        # print(old_move_stack)

        for index in range(self.__MIN_SAN_LENGTH, self.__MAX_SAN_LENGTH):
            for x in range(index, self.__MAX_SAN_LENGTH):
                # next_move = next_move[:x]
                try:
                    # print(next_move[index:x])
                    board.push_san(next_move[index:x])
                    break
                except (chess.InvalidMoveError, chess.IllegalMoveError, chess.AmbiguousMoveError):
                    pass

        if old_move_stack == board.move_stack:
            # print(old_move_stack)
            # print(board.move_stack)
            raise chess.InvalidMoveError
        return board

    def __extract_legal_moves(self, board):
        input_string = str(board.legal_moves)
        match = re.search(r'\((.*?)\)', input_string)  # match content inside brackets
        if match:
            legal_moves_str = match.group(1)  # extract matched group
        else:
            legal_moves_str = ""  # no match, empty string
        return legal_moves_str

    def extract_token_data(self, json_string):
        data = json.loads(json_string)
        token_logprobs = data["choices"][0]["logprobs"]["token_logprobs"]
        tokens = data["choices"][0]["logprobs"]["tokens"]

        """Creates a list of tuples from two lists of equal length"""
        if len(token_logprobs) != len(tokens):
            raise ValueError("Lists must be of equal length")
        return [(tokens[i], token_logprobs[i]) for i in range(len(token_logprobs))]

    def calculate_prob_sum_str(self, string: str, tuple_list):
        # Check if the string is in the first part of any tuple in the list

        sorted_list = sorted(tuple_list, key=lambda x: len(x[0]), reverse=True)

        prefix = ""
        temp_str = ""
        prob_sum = 0

        while len(prefix) < len(string):
            test_str = copy.copy(prefix)
            for i in range(len(sorted_list)):
                temp_str = prefix + sorted_list[i][0]
                if string.startswith(temp_str):
                    prob_sum = prob_sum + sorted_list[i][1]
                    prefix = temp_str
            if test_str == prefix:
                raise ValueError("String cant be combined from tokens")

        return [string, prob_sum]

    def get_legal_moves_list(self, board: chess.Board):
        legal_moves = self.__extract_legal_moves(board)
        legal_moves_list = legal_moves.split(", ")
        return legal_moves_list
