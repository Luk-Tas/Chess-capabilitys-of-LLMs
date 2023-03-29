import copy

import chess


class ComEngineLLM:
    __STYLE1_PROMPT1 = "Chess Game: "
    __STYLE1_PROMPT2 = "\nA chess "
    __STYLE1_PROMPT3 = " would play the move:"
    __STYLE2_PROMPT1 = "The following is a chess game between two chess "
    __STYLE2_PROMPT2 = "s:\n"
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
