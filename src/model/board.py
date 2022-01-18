import numpy
import numpy as np

from model.move import Move


class Board(object):
    x = 1
    o = -1

    def __init__(self, state: numpy.ndarray, next_to_move=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please input the right parameters!")

        self.board_size = state.shape[0]
        self.state = state
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        row_sum = np.sum(self.state, 0)
        col_sum = np.sum(self.state, 1)
        diag_sum_tl = self.state.trace()
        diag_sum_tr = self.state[::-1].trace()

        if any(row_sum == self.board_size) or any(
                col_sum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1
        elif any(row_sum == -self.board_size) or any(
                col_sum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:
            return -1

        elif np.all(self.state != 0):
            return 0
        else:
            return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        if move.value != self.next_to_move:
            print("board.next_to_move: " + str(self.next_to_move) + " move.value: " + str(move.value))
            return False

        x_in_range = self.board_size > move.x_coor >= 0
        if not x_in_range:
            return False

        y_in_range = self.board_size > move.y_coor >= 0
        if not y_in_range:
            return False

        return self.state[move.x_coor, move.y_coor] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.state + " is not legal")
        new_state = np.copy(self.state)
        new_state[move.x_coor, move.y_coor] = move.value

        if self.next_to_move == Board.x:
            next_to_move = Board.o
        else:
            next_to_move = Board.x

        return Board(new_state, next_to_move)

    def get_legal_actions(self):
        """
        :return: list of class Move
        """
        indices = np.where(self.state == 0)
        return [Move(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]
