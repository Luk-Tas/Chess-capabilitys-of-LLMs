import copy

import chess


class ComEngineLLM:
    __PROMPT1 = "Chess Game: "
    __PROMPT2 = "\nA chess "
    __PROMPT3 = " would play the move:"
    __MAX_SAN_LENGTH = 7
    __MIN_SAN_LENGTH = 1
    __COUNT_DOWN_STEP = -1

    def engine_to_llm(self, board: chess.Board, difficulty):
        prompt = self.__PROMPT1
        temporary_board = chess.Board()
        move_list = temporary_board.variation_san(board.move_stack)
        prompt = prompt + move_list + self.__PROMPT2 + difficulty + self.__PROMPT3
        return prompt

    def llm_to_engine(self, board: chess.Board, next_move: str):
        old_move_stack = copy.copy(board.move_stack)
        print(old_move_stack)
        for x in range(self.__MAX_SAN_LENGTH, self.__MIN_SAN_LENGTH, self.__COUNT_DOWN_STEP):
            next_move = next_move[:x]
            try:
                board.push_san(next_move)
                break
            except (chess.InvalidMoveError, chess.IllegalMoveError):
                pass
        if old_move_stack == board.move_stack:
            print(old_move_stack)
            print(board.move_stack)
            raise chess.InvalidMoveError
        return board
