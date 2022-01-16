from model.Board import Board
from model.Move import Move
from view.Graphics import *
import numpy as np

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
