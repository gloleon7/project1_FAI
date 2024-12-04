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
    Determines which player's turn it is. 'X' always goes first, 
    so if the counts of 'X' and 'O' are equal, it's 'X's turn. Otherwise, it's 'O's turn.
    """
    x_count = sum(row.count(X) for row in board) #row.count(X) counts how many times X appears in that row
    #sum() counts the amount of Xs
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
   Returns the set of all possible actions (i, j) on the board. 
   These are all the cells that are currently empty.
    """
    moves = set() #moves is a storage of positions which are free
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j)) #adds to move the position of the free position
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]
    i, j = action
    current_player = player(board)
    
    # Ensure the move is valid (cell is empty)
    if new_board[i][j] != EMPTY:
        raise Exception("Invalid move!")
    
    # Apply the current player's move
    new_board[i][j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:  # If there's a winner
        return True
    for row in board:
        if EMPTY in row:  # If there are empty cells, the game is still in progress
            return False
    return True  # No winner and no empty cells -> tie


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is over, return None
    if terminal(board):
        return None
    
    # Max player (X) and Min player (O)
    current_player = player(board)
    
    if current_player == X:
        best_value = -math.inf
        best_move = None
        for move in actions(board): # for each possible movement ,we create a new board after moving
            new_board = result(board, move)
            # we calculate the utility of the movement
            move_value = min_value(new_board)
            if move_value > best_value: #if we find another value which is better, 
                #we change it
                best_value = move_value
                best_move = move
        return best_move
    else:  # For 'O'
        best_value = math.inf
        best_move = None
        for move in actions(board):
            new_board = result(board, move)
            move_value = max_value(new_board)
            if move_value < best_value:
                best_value = move_value
                best_move = move
        return best_move

def max_value(board):
    """
    Returns the max utility for a board (used for maximizing player X).
    """
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for move in actions(board):
        new_board = result(board, move)
        v = max(v, min_value(new_board))
    return v

def min_value(board):
    """
    Returns the min utility for a board (used for minimizing player O).
    """
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for move in actions(board):
        new_board = result(board, move)
        v = min(v, max_value(new_board))
    return v
