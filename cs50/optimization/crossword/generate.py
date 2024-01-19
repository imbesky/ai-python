import copy
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)

        domain[variable] = {set of possible words}
        """
        for variable in self.domains:
            proper_length = variable.length
            for value in self.domains[variable].copy():
                if len(value) != proper_length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap_location = self.crossword.overlaps[x, y]

        if overlap_location is not None:
            for x_value in self.domains[x].copy():
                satisfy = False
                for y_value in self.domains[y]:
                    if x_value[overlap_location[0]] == y_value[overlap_location[1]]:
                        satisfy = True
                        break
                if not satisfy:
                    self.domains[x].remove(x_value)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = set()
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        arcs.add((x, y))
        for arc in arcs:
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        원본(효율성을 위해 수정함/dict()는 키 중복이 안되니까):
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return true
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        done_words = set()
        done_combination = set()
        for variable in assignment:
            word = assignment[variable]
            # 1. all values are distinct
            if word in done_words:
                return False
            done_words.add(word)
            # 2. every value is the correct length
            if len(word) != variable.length:
                return False
            # 3. no conflicts between neighboring variables
            neighbors = self.crossword.neighbors(variable)
            for neighbor in assignment:
                if (variable, neighbor) not in done_combination and neighbor in neighbors:
                    overlap = self.crossword.overlaps[variable, neighbor]
                    if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
                    done_combination.add((neighbor, variable))
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        counts = dict()
        values = []
        count = 0
        neighbors = self.crossword.neighbors(var)
        for value in self.domains[var]:
            for neighbor in self.domains:
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap is not None:
                        for neighbor_value in self.domains[neighbor]:
                            if neighbor_value == value:
                                count += 1
                                continue
                            if value[overlap[0]] != neighbor_value[overlap[1]]:
                                count += 1
                    else:
                        if value in self.domains[neighbor]:
                            count += 1
            counts[value] = count
            values.append(value)
        values.sort(key=lambda item: counts[item])
        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_remain = len(self.crossword.words)
        result_var = None
        for variable in self.crossword.variables:
            if variable not in assignment:
                if len(self.domains[variable]) < min_remain:
                    result_var = variable
                    min_remain = len(self.domains[variable])
                elif len(self.domains[variable]) == min_remain and self.crossword.neighbors(
                        variable) > self.crossword.neighbors(result_var):
                    result_var = variable
        return result_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        def inference(var):
            unassigned = set()
            original = dict()
            for v in self.crossword.variables:
                if v not in assignment:
                    unassigned.add(v)

            def restore():
                for origin in original:
                    self.domains[origin] = original[origin]

            for v in unassigned:
                original[v] = self.domains[v]
                if not self.ac3([(var, v)]):
                    restore()
                    return None
            inferred = dict()
            for v in unassigned:
                if len(self.domains[v]) == 1:
                    for i in self.domains[v]:
                        inferred[v] = i
            restore()
            return inferred

        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.domains[variable]:
            assignment[variable] = value
            inferences = None
            if self.consistent(assignment):
                inferences = inference(variable)
            if inferences is not None:
                for key in inferences:
                    assignment[key] = inferences[key]
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[variable]
            if inferences is not None:
                for key in inferences:
                    del assignment[key]
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
