from Board import *
from collections import defaultdict


class TreeNode(object):
    def __init__(self, state: Board, parent=None):
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions
