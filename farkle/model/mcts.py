from state import *


class Node(object):
    def __init__(self, state: State, parent=None):
        self.state = state
        self.number_visit = 0
        self.value = 0
        self.parent = parent
        self.children = []

    @property
    def average_value(self):
        if len(self.children) == 0:
            return self.value
        sum_score = 0
        for node in self.children:
            sum_score += node.value
        return sum_score / len(self.children)

    def expand(self):
        next_state = self.state.next_states.pop()
        child_node = Node(next_state, self)
        self.children.append(child_node)
        return child_node
