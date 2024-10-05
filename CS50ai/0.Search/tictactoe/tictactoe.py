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
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)
    
    if count_X <= count_O:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = [row[:] for row in board]  # MAKE A DEEP COPY
    i, j = action
    copy_board[i][j] = player(board)

    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        # Check all columns
        player = board[0][i]
        if player != EMPTY and all(board[row][i] == player for row in range(3)):
            return player

        # Check all rows
        player = board[i][0]
        if player != EMPTY and all(board[i][col] == player for col in range(3)):
            return player

    # Check diagonals
    player = board[0][0]
    if player != EMPTY and all(board[x][x] == player for x in range(3)):
        return player

    player = board[0][2]
    if player != EMPTY and all(board[x][2 - x] == player for x in range(3)):
        return player

    # If no winner, return None
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # CHECK FOR A WINNER
    if winner(board):
        return True
    
    # CHECK IF ALL CELLS ARE FULL
    if all(cell != EMPTY for row in board for cell in row):
        return True
    
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board) 
    
    if current_player == X:
        _, action = max_value(board)
        return action
    else:
        _, action = min_value(board)
        return action

def max_value(board):
    if terminal(board):
        return utility(board), None  # BASE-CASE(WHEN WHOLE BOARD IS FILLED, RETURNS SCORE)
    
    score = -float('inf')
    best_action = None
    
    for action in actions(board):
        min_val, _ = min_value(result(board, action))  # PUT IN OTHERS SHOES(TO KNOW WORST THING CAN HAPPEN)
    
        if min_val > score:  # MAX-PLAYER WILL MAXIMIZE THE SCORE.
            score = min_val
            best_action = action  # BEST-ACTION IN ALL THE ACTIONS WILL BE STORED.
            
    return score, best_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    
    score = float('inf')
    best_action = None
    
    for action in actions(board):
        max_val, _ = max_value(result(board, action))  # PUT IN OTHERS SHOES(TO KNOW WORST THING CAN HAPPEN)

        if max_val < score:  # MIN-PLAYER WILL MINIMIZE THE SCORE.
            score = max_val
            best_action = action  # BEST-ACTION IN ALL THE ACTIONS WILL BE STORED.
            
    return score, best_action
