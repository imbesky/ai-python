"""
Tic Tac Toe Player
"""
import copy
import math
import random

import util

X = "X"
O = "O"
players = [X, O]
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
    if blank_of(board) % 2 == 1:
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


def accept_action(target_player, board, action):
    if board[action[0]][action[1]] != EMPTY:
        raise AttributeError('invalid action')
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = target_player
    return result_board


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    return accept_action(player(board), board, action)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != EMPTY:
            return row[0]

    for index in range(len(board[0])):
        column = []
        for row in board:
            column.append(row[index])
        if column.count(column[0]) == len(column) and column[0] != EMPTY:
            return column[0]

    right_diagonal = []
    left_diagonal = []
    for index in range(len(board)):
        right_diagonal.append(board[index][index])
        left_diagonal.append(board[index][len(board[index]) - index - 1])
    if right_diagonal.count(right_diagonal[0]) == len(right_diagonal)\
            and right_diagonal[0] != EMPTY:
        return right_diagonal[0]
    if left_diagonal.count(left_diagonal[0]) == len(left_diagonal) \
            and left_diagonal[0] != EMPTY:
        return left_diagonal[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    if blank_of(board) != 0:
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


def switch_player(current_player):
    for candidate in players:
        if current_player != candidate:
            return candidate


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    frontier = util.StackFrontier()
    current_player = player(board)
    winnable_actions = []
    winnable_actions_set = set()
    minimum_move = 0

    initial_actions = actions(board)
    for action in initial_actions:
        frontier.push(
            util.Node(action, 1,
                      accept_action(current_player, board, action), current_player))

    while frontier.size() != 0:
        node = frontier.pop()

        if node.move > minimum_move != 0:
            continue

        win = winner(node.board)
        if win is None and blank_of(node.board) == 0:
            continue
        if win is not None and win == current_player:
            winnable_actions.append(node.root_action)
            minimum_move = node.move
            continue

        next_player = switch_player(node.player)
        for action in actions(node.board):
            frontier.push(
                util.Node(node.root_action, node.move + 1,
                          accept_action(next_player, node.board, action),
                          next_player))

    if len(winnable_actions) == 0:
        return initial_actions[0]

    optimal_action = None
    max_frequency = 0
    for action in initial_actions:
        this_frequency = winnable_actions.count(action)
        if this_frequency > max_frequency:
            max_frequency = this_frequency
            optimal_action = action

    return optimal_action
