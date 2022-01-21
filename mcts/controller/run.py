from view.graphics import *


def init_board():
    init_state = np.zeros((3, 3))
    ini_board = Board(state=init_state, next_to_move=1)
    init_root = TreeNode(ini_board)
    init_mcts = TreeSearch(init_root)
    init_best_node = init_mcts.best_action(1000)
    c_board = init_best_node.board

    return c_board


board = init_board()
graphics(board.state)

while True:
    move1 = get_action(board, board.next_to_move)
    board = board.move(move1)

    root = TreeNode(board)
    mcts = TreeSearch(root)
    best_node = mcts.best_action(1000)
    board = best_node.board

    graphics(board.state)
    if judge(board) == 1:
        break
    elif judge(board) == -1:
        continue

