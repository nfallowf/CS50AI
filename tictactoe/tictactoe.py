"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If there are an equal number of xs and os on the board, its xs turn else its os
    if sum(list.count(X) for list in board) == sum(list.count(O) for list in board):
        return X
    else :
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError(action)
    i, j = action
    newBoard = copy.deepcopy(board)
    if player(board) == X:
        newBoard[i][j] = X
        return newBoard
    else:
        newBoard[i][j] = O
        return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for horizontal winner
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
    # Check vertical winner
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[0][j] != EMPTY:
            return board[0][j]
    # Check diagonal winners
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or not any(EMPTY in list for list in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    elif terminal(board):
        return 0

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        max = -100
        best_move = None
        for action in actions(board):
            move_value = min_value(result(board, action))
            if move_value == 1: # No need to consider other moves if this move can win
                return action
            if move_value > max:
                max = move_value
                best_move = action
    else:
        min = 100
        best_move = None
        for action in actions(board):
            move_value = max_value(result(board, action))
            if move_value == -1: # No need to consider other moves if this move can win
                return action
            if move_value < min:
                min = move_value
                best_move = action
    return best_move
