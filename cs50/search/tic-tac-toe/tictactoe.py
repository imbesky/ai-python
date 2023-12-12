"""
Tic Tac Toe Player
"""

import math
import util

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


def blank_of(board):
    blank = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                blank += 1
    return blank


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if math.remainder(blank_of(board), 2) == 1:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (row: i, cell: j) available on the board.
    """
    possible = []
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if board[row][cell] == EMPTY:
                possible.append((row, cell))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        return AttributeError('invalid action')
    result_board = board
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(row[0]) == len(row):
            return row[0]

    for index in board[0]:
        column = []
        for row in board:
            column.append(row[index])
        if column.count(column[0]) == len(column):
            return column[0]

    right_diagonal = []
    left_diagonal = []
    for index in range(len(board)):
        right_diagonal.append(board[index][index])
        left_diagonal.append(board[index][len(board[index]) - index])
    if right_diagonal.count(right_diagonal[0]) == len(right_diagonal):
        return right_diagonal[0]
    if left_diagonal.count(left_diagonal[0]) == len(left_diagonal):
        return left_diagonal[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    if blank_of(board) is not 0:
        return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    if win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    frontier = util.StackFrontier()
    current_player = player(board)
    optimal_action = None
    minimum_move = 0

    initial_actions = actions(board)
    for action in initial_actions:
        frontier.push(util.Node(action, action, 1, result(board, action)))

    while frontier.size() is not 0:
        node = frontier.pop()

        if node.move >= minimum_move and minimum_move is not 0:
            continue

        if terminal(node.board):
            if winner(node.board) == current_player:
                optimal_action = node.root_action
                minimum_move = node.move
                continue
            continue

        for action in actions(node.board):
            frontier.push(
                util.Node(action, node.root_action, node.move + 1, result(node.board, action)))

    if optimal_action is None:
        return initial_actions[0]

    return optimal_action
