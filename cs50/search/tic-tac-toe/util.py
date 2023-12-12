class Node():
    def __init__(self, action, root_action, move, board):
        self.action = action
        self.root_action = root_action
        self.move = move
        self.board = board


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def push(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def pop(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def size(self):
        return len(self.frontier)