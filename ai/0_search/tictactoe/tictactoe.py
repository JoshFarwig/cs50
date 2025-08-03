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
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if terminal(board) == True:
        return None

    # since X always goes first, we can assume that when there are odd amount of
    # empty spaces, it is X's turn. when there is an even amount of empty spaces, it's
    # O's turn.
    empty_count = sum(1 for row in board for column in row if column == EMPTY)

    return X if empty_count % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # possible moves are all empty spaces
    # any return value is acceptable if terminal board is input (i.e end of game)

    if terminal(board):
        return set()

    actions = {
        (i, j)
        for i in range(len(board))
        for j in range(len(board))
        if board[i][j] == EMPTY
    }

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # if action is not a valid action (i.e. a space is already occupuied), should throw exception
    # returned board state = new board, make a deep copy of the input board state, let the player
    # know whos turn it is, then with the action, return the new board state

    i, j = action
    # check if space is taken
    if board[i][j] != EMPTY:
        raise Exception("Space already occupied by a player")

    # check if action out of bounds
    if i < 0 or i >= len(board) or j < 0 and j >= len(board):
        raise Exception("Action is outside of board space")

    result_board = copy.deepcopy(board)
    result_board[i][j] = player(board)

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check row wins
    for row in board:
        if row[0] != EMPTY and all(cell == row[0] for cell in row):
            return row[0]

    # check for column wins
    for j in range(len(board)):
        column = [board[i][j] for i in range(len(board))]
        if column[0] != EMPTY and all(cell == column[0] for cell in column):
            return column[0]

    # check for diagonal wins
    main_diag = [board[i][i] for i in range(len(board))]
    reverse_diag = [board[i][2 - i] for i in range(len(board))]

    if main_diag[0] != EMPTY and all(cell == main_diag[0] for cell in main_diag):
        return main_diag[0]

    if reverse_diag[0] != EMPTY and all(
        cell == reverse_diag[0] for cell in reverse_diag
    ):
        return reverse_diag[0]

    # If no wins, just return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if winner exists or tie has occured,
    # return True, else False
    return winner(board) is not None or all(
        cell != EMPTY for row in board for cell in row
    )


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # utility will only be called on board if terminal(board) = true
    if not terminal(board):
        raise Exception("Utility cannot be used on a non-terminal state")

    winner_result = winner(board)

    match winner_result:
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # TODO - Add A-B Pruning

    # if there are multiple optimal moves of same value, any arb one can be chosen
    # if board is terminal board, should return None
    if terminal(board):
        return None
    # best move maximizing player can make
    alpha = float("-inf")
    # best move minimizing player can make
    beta = float("inf")

    def max_value(board, alpha, beta):
        # base-case
        if terminal(board):
            return utility(board)

        v = float("-inf")

        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)

            v = max(v, value)
            alpha = max(alpha, v)

            if alpha >= beta:
                break

        return v

    def min_value(board, alpha, beta):
        # base case
        if terminal(board):
            return utility(board)

        v = float("inf")

        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)

            v = min(v, value)
            beta = min(v, beta)

            if alpha >= beta:
                break

        return v

    # determine player
    player_type = player(board)
    best_action = None

    if player_type == X:
        best_value = float("-inf")
        # what are all of my actions
        for action in actions(board):
            # assuming O plays optimally, the potiental results from
            # these actions are the min board states...
            value = min_value(result(board, action), alpha, beta)
            # X wants highest value in the min's so
            if value > best_value:
                best_value = value
                best_action = action

    if player_type == O:
        best_value = float("inf")
        # what are all of my actions
        for action in actions(board):
            # assuming X plays optimally, the potiental results from
            # these actions are the max board states...
            value = max_value(result(board, action), alpha, beta)
            # O wants lowest value in the max's so
            if value < best_value:
                best_value = value
                best_action = action

    return best_action
