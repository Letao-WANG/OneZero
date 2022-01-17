from model.board import Board
from model.move import Move
from model.TreeNode import TreeNode
from model.TreeSearch import TreeSearch
import numpy as np


def graphics(state):
    """
    :param state: np.array() which is the state of board
    """
    for i in range(3):
        print("")
        print("{0:3}".format(i).center(8) + "|", end='')
        for j in range(3):
            if state[i][j] == 0:
                print('_'.center(8), end='')
            if state[i][j] == 1:
                print('X'.center(8), end='')
            if state[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def init_board():
    init_state = np.zeros((3, 3))
    board = Board(state=init_state, next_to_move=1)
    root = TreeNode(board)
    mcts = TreeSearch(root)
    best_node = mcts.best_action(1000)
    c_board = best_node.board

    return c_board


def get_action(board: Board, next_to_move):
    try:
        location = input("Your move: ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 2:
            return -1
        x = location[0]
        y = location[1]
        move = Move(x, y, next_to_move)
    except Exception as e:
        move = -1
    if move == -1:
        print("invalid move")
        move = get_action(board, next_to_move)

    if not board.is_move_legal(move):
        print("illegal move")
        move = get_action(board, next_to_move)

    return move


def judge(board):
    if board.is_game_over():
        if board.game_result == 1:
            print("You lose!")
        if board.game_result == 0:
            print("Tie!")
        if board.game_result == -1:
            print("You Win!")
        return 1
    else:
        return -1
