from model.Board import Board
from model.Move import Move
import numpy as np


def init_board():
    state = np.zeros((3, 3))
    board = Board(state=state, next_to_move=1)

    return board


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


def get_action(board : Board, next_to_move):
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


c_board = init_board()
graphics(c_board.state)

while True:
    move1 = get_action(c_board, c_board.next_to_move)
    c_board = c_board.move(move1)
    graphics(c_board.state)
    if judge(c_board)==1:
        break
    elif judge(c_board)==-1:
        continue