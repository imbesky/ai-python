"""
Tic Tac Toe Player
"""
import copy

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


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise AttributeError('invalid action')
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board


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
    if right_diagonal.count(right_diagonal[0]) == len(right_diagonal) \
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


def winnable_actions_of(board):
    win_actions = set()
    for action in actions(board):
        if winner(result(board, action)) == player(board):
            win_actions.add(action)
    return win_actions


def not_losable_actions_of(board):
    not_losable_actions = set()
    for action in actions(board):
        next_board = result(board, action)
        if len(winnable_actions_of(next_board)) == 0:
            not_losable_actions.add(action)
    return not_losable_actions


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    winnable_actions = winnable_actions_of(board)
    if len(winnable_actions) != 0:
        return winnable_actions.pop()

    frontier = util.StackFrontier()
    winnable_actions = dict()
    drawable_actions = dict()
    losable_actions = dict()
    root_actions = not_losable_actions_of(board)
    for action in root_actions:
        frontier.push(util.Node(action, 1, result(board, action)))
        winnable_actions[action] = (0, 0)  # move, count
        drawable_actions[action] = (0, 0)
        losable_actions[action] = (0, 0)
    current_player = player(board)
    explored = []

    def update(target, root, move):
        if move < target[root][0] or target[root][0] == 0:
            target[root] = (move, 1)
        elif move == target[root][0]:
            target[root] = (move, target[root][1] + 1)

    while frontier.size() != 0:
        node = frontier.pop()

        if node.board in explored:
            continue

        explored.append(node.board)

        if terminal(node.board):
            win = winner(node.board)
            if win == current_player:
                update(winnable_actions, node.root_action, node.move)
                continue
            if win is None:
                update(drawable_actions, node.root_action, node.move)
                continue
            update(losable_actions, node.root_action, node.move)
            continue

        not_losable_actions = not_losable_actions_of(node.board)
        for action in not_losable_actions:
            frontier.push(util.Node(node.root_action, node.move + 1, result(node.board, action)))

    max_count = 0
    optimal_action = None

    # to win
    for action in root_actions:
        if ((winnable_actions[action][0] < losable_actions[action][0]
             or losable_actions[action][0] == 0)
                and winnable_actions[action][1] > max_count != 0):
            max_count = winnable_actions[action][1]
            optimal_action = action

    # to draw
    if optimal_action is None:
        max_count = 0
        for action in root_actions:
            if ((drawable_actions[action][0] < losable_actions[action][0]
                 or losable_actions[action][0] == 0)
                    and drawable_actions[action][1] > max_count != 0):
                max_count = drawable_actions[action][1]
                optimal_action = action

    # there is no way to win
    if optimal_action is None:
        try:
            optimal_action = root_actions.pop()
        except KeyError:
            optimal_action = actions(board).pop()

    return optimal_action
