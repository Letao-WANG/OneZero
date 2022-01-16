from model.TreeNode import TreeNode


class TreeSearch:
    def __init__(self, node: TreeNode):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            result = v.rollout()
            v.backpropagate(result)
        # exploitation only
        return self.root.best_child(c_param=0)

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node