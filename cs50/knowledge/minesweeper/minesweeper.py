import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if count == len(cells) then all the cells are mine
        if self.count == len(self.cells):
            for cell in self.cells:
                self.mines.add(cell)
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if count == 0 then there is no mine
        if self.count == 0:
            for cell in self.cells:
                self.safes.add(cell)
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        the function should update the sentence so that cell is no longer in the sentence,
        but still represents a logically correct sentence given that cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        surroundings = []
        for row in range(max(cell[0] - 1, 0), min(cell[0] + 2, self.height)):
            for column in range(max(cell[1] - 1, 0), min(cell[1] + 2, self.width)):
                surroundings.append((row, column))
        surroundings.remove(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #       based on the value of `cell` and `count`
        def add_knowledge(sentence):
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

        def initial_knowledge(cells, counts):
            accepted = []
            for c in cells:
                if c in self.safes:
                    continue
                elif c in self.mines:
                    counts -= 1
                    continue
                accepted.append(c)
            if len(accepted) == 0:
                return
            return add_knowledge(Sentence(accepted, counts))

        initial_knowledge(surroundings, count)

        # 4) mark any additional cells as safe or as mines
        #       if it can be concluded based on the AI's knowledge base
        def additional_marking(sentence):
            for mine in sentence.known_mines():
                self.mark_mine(mine)
            for safe in sentence.known_safes():
                self.mark_safe(safe)

        # 5) add any new sentences to the AI's knowledge base
        #       if they can be inferred from existing knowledge
        def infer_new_sentence(sentence):
            new_knowledge = []
            duplicate = 0
            for another_sentence in self.knowledge:
                if (0 < len(another_sentence.cells) < len(sentence.cells) and
                        another_sentence.cells.issubset(sentence.cells)):
                    new_knowledge.append(Sentence(
                        sentence.cells.difference(another_sentence.cells),
                        sentence.count - another_sentence.count))
                elif sentence == another_sentence:
                    if duplicate > 0:
                        another_sentence.cells = set()
                        continue
                    duplicate += 1
            for new_sentence in new_knowledge:
                add_knowledge(new_sentence)

        def ai_thinking():
            for sentence in self.knowledge:
                additional_marking(sentence)
                infer_new_sentence(sentence)
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)

        ai_thinking()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for h, w in itertools.product(range(self.height), range(self.width)):
            if (h, w) not in self.moves_made and (h, w) not in self.mines:
                return h, w
        return None
