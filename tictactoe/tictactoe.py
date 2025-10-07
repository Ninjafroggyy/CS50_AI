"""
Tic Tac Toe Player
"""

import math
import random

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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return X if x_count == o_count else O

"""
def actions(board):
    ""
    Returns set of all possible actions (i, j) available on the board.
    ""
    # If the game is already over there are no moves left
    if terminal(board):
        return set()

    moves = set()

    # Loop through each row and each column, if cell is empty add co-ordinates of all possible actions
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))

    return moves
"""


def actions(board):
    """
    Returns a randomised list of all possible actions (i, j) available on the board.
    """

    # If the game is already over, there are no moves left
    if terminal(board):
        return []

    # Gather all empty cells on the board
    moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY]

    # Shuffle them so the AI doesn't always make the same move order
    random.shuffle(moves)

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Check move can be made by looking at available cells
    if action not in actions(board):
        raise ValueError("Action not available")

    turn = player(board)

    # Make a new copy of the board
    new_board = [row[:] for row in board]

    new_board[i][j] = turn

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []

    for index in range(3):
        # Row index
        lines.append([board[index][0], board[index][1], board[index][2]])

        # Column index
        lines.append([board[0][index], board[1][index], board[2][index]])

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    # Check each line, if all three are equal and not EMPTY
    for line in lines:
        if line[0] is not None and line[0] == line[1] == line[2]:
            return line[0]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If either X or O have three in a row the game is over
    if winner(board) is not None:
        return True

    # If there is not three in a row check for EMPTY cells
    for row in board:
        for cell in row:

            # If there is still empty cells the game continues
            if cell is EMPTY:
                return False

    # If there are no EMPTY cells left, it's a draw and game is over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    score, best_move = best_outcome(board)

    return best_move


def best_outcome(board):
    """
    Calculate the best outcome for the player to move on the board
    """
    # If the game has completed return the score
    if terminal(board):
        return utility(board), None

    turn = player(board)
    optimal_move = None

    # X's turn (maximises the score)
    if turn == X:
        # Start with lowest possible value
        best_score = -math.inf

        # Try all available moves
        for move in actions(board):
            child_board = result(board, move)
            child_score, _ = best_outcome(child_board)

            # Record if this move gives a better score for X player
            if child_score > best_score:
                best_score = child_score
                optimal_move = move

            # If the best score is 1 then X has won the game
            if best_score == 1:
                break
    # O's turn (minimises the score)
    else:
        # Start with the highest possible number
        best_score = math.inf

        # Try all available moves
        for move in actions(board):
            child_board = result(board, move)
            child_score, _ = best_outcome(child_board)

            # If this move gives a lower score then record
            if child_score < best_score:
                best_score = child_score
                optimal_move = move

            # If the best score is -1 then O has won the game
            if best_score == -1:
                break

    return best_score, optimal_move

