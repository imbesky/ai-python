class Node():
    def __init__(self, root_action, move, board):
        self.root_action = root_action
        self.move = move
        self.board = board


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def push(self, node):
        self.frontier.append(node)

    def contains_board(self, board):
        return any(node.board == board for node in self.frontier)

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


class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def enqueue(self, node):
        self.frontier.append(node)

    def contains_board(self, board):
        return any(node.board == board for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def dequeue(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

    def size(self):
        return len(self.frontier)
