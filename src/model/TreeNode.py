from model.board import *
from collections import defaultdict


def rollout_policy(possible_moves):
    return possible_moves[np.random.randint(len(possible_moves))]


class TreeNode(object):
    def __init__(self, board: Board, parent=None):
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self.board = board
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        """list of Move"""
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.board.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.board.next_to_move]
        loses = self._results[-1 * self.parent.board.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        """
        expand one child node
        :return: child node
        """
        action = self.untried_actions.pop()
        next_board = self.board.move(action)
        child_node = TreeNode(next_board, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.board.is_game_over()

    def rollout(self):
        """
        Get the result of current Board of Node
        :return: the result of board, 1, -1, 0 or None
        """
        current_rollout_board = self.board
        while not current_rollout_board.is_game_over():
            possible_moves = current_rollout_board.get_legal_actions()
            action = rollout_policy(possible_moves)
            current_rollout_board = current_rollout_board.move(action)
        return current_rollout_board.game_result

    def backpropagate(self, result):
        """
        :param result: result of board
        :return:
        """
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]
