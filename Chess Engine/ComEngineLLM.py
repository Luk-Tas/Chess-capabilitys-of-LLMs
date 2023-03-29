import copy

import chess


class ComEngineLLM:
    __PROMPT1 = "Chess Game: "
    __PROMPT2 = "\nA chess "
    __PROMPT3 = " would play the move:"
    __MAX_SAN_LENGTH = 11
    __MIN_SAN_LENGTH = 1

    # currently unused
    __COUNT_DOWN_STEP = -1

    def engine_to_llm(self, board: chess.Board, difficulty):
        prompt = self.__PROMPT1
        temporary_board = chess.Board()
        move_list = temporary_board.variation_san(board.move_stack)
        prompt = prompt + move_list + self.__PROMPT2 + difficulty + self.__PROMPT3
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
                except (chess.InvalidMoveError, chess.IllegalMoveError):
                    pass

        if old_move_stack == board.move_stack:
            # print(old_move_stack)
            # print(board.move_stack)
            raise chess.InvalidMoveError
        return board
