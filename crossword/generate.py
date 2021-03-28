import sys
from crossword import *
from queue import Queue

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        """
        for domain in self.domains:
            for word in self.domains[domain].copy():
                if len(word) != domain.length:
                    self.domains[domain].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps[x, y]
        if overlaps == None:
            return False
        revised = False
        for word1 in self.domains[x].copy():
            for word2 in self.domains[y]:
                if word1[overlaps[0]] == word2[overlaps[1]]:
                    break;
            else:
                self.domains[x].remove(word1)
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
        q = Queue()
        if arcs == None:
            for domain in self.domains:
                neighbors = self.crossword.neighbors(domain)
                for neighbor in neighbors:
                    q.put((domain, neighbor))
        else:
            for arc in arcs:
                q.put(arc)
        while not q.empty():
            (X, Y) = q.get()
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                neighbors = []
                for neighbor in self.crossword.neighbors(X):
                    if neighbor != Y:
                        neighbors.append(neighbor)
                for neighbor in neighbors:
                    q.put((neighbor, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(self.domains) == len(assignment)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable1 in assignment:
            word1 = assignment[variable1]
            if variable1.length != len(word1):
                return False

            for variable2 in assignment:
                word2 = assignment[variable2]
                if variable1 != variable2:
                    if word1 == word2:
                        return False

                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap is not None:
                        a, b = overlap
                        if word1[a] != word2[b]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        weighted_values = dict.fromkeys(self.domains[var], 0)
        neighbor_vars = self.crossword.neighbors(var) - assignment.keys()

        for word1 in self.domains[var]:
            num_ruled_out = 0
            for neighbor in neighbor_vars:
                for word2 in self.domains[neighbor]:
                    if word1 == word2:
                        num_ruled_out += 1
                    overlap = self.crossword.overlaps[var, neighbor]
                    a, b = overlap
                    if word1[a] != word2[b]:
                        num_ruled_out += 1

            weighted_values[word1] = num_ruled_out
        sorted_weighted_values = sorted(weighted_values.items(), key=lambda x: x[1])
        values = [x[0] for x in sorted_weighted_values]

        return values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        return_var = None
        length = float('inf')
        tied = []
        for var in self.crossword.variables:
            if var not in assignment:
                if len(self.domains[var])  < length:
                    tied.clear()
                    length = len(self.domains[var])
                    return_var = var
                elif len(self.domains[var]) == length:
                    tied.append(var)

        if len(tied) != 0:
            degree = float('-inf')
            for var in tied:
                if len(self.crossword.neighbors(var)) > degree:
                    degree = len(self.crossword.neighbors(var))
                    return_var = var

        return return_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
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
