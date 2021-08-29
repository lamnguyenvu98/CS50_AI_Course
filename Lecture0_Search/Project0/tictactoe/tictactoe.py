"""
Tic Tac Toe Player
"""

import math

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
    if terminal(board):
        return   
    track = {}
    track[X] = 0
    track[O] = 0
    for states in board:
        for state in states:
            if state is not None:
                track[state] += 1
            
    if track[O] < track[X]:
        return O
    return X
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is None:
                action.add((i, j))
    return action
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    from copy import deepcopy
    result = deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    import numpy as np
    b = np.array(board)
    if np.all(O == b, axis=0).sum() or np.all(O == b, axis=1).sum()\
        or all(b.diagonal() == O) or all(np.rot90(b).diagonal() == O):
        return(O)
    elif np.all(X == b, axis=0).sum() or np.all(X == b, axis=1).sum()\
        or all(b.diagonal() == X) or all(np.rot90(b).diagonal() == X):
        return(X)
    return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not any(EMPTY in sub for sub in board):
        return True
    else: return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if terminal(board):
        return 1 if win == X else -1 if win == O else 0
    #raise NotImplementedError

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    best = float('inf')
    for action in actions(board):
        current_board = result(board, action)
        best = min(best, max_value(current_board, alpha, beta))
        beta = min(beta, best)
        if beta <= alpha: break
    return best
        

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    best = float('-inf')
    for action in actions(board):
        current_board = result(board, action)
        best = max(best, min_value(current_board, alpha, beta))
        alpha = max(alpha, best)
        if beta <= alpha: break
    return best

def minimax(board): # alpha-beta pruining
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    alpha, beta = float('-inf'), float('inf')
    if player(board) == X:
        arr = []
        for action in actions(board):
            arr.append([min_value(result(board, action), alpha, beta), action])
        return sorted(arr, key=lambda x: x[0], reverse=True)[0][1]
    elif player(board) == O:
        arr = []
        for action in actions(board):
            arr.append([max_value(result(board, action), alpha, beta), action])
        return sorted(arr, key=lambda x: x[0])[0][1]
    #raise NotImplementedError
