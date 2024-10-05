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
        self.enforce_node_consistency() # FOR NODE CONSISTENCY(UNARY CONSTRAINS).
        self.ac3() # FOR ARC-CONSISTENCY(BINARY CONSTRAINS)
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` to only allow values that satisfy the unary constraints 
        (i.e., the length of the word must match the length of the variable).
        """
        for var in self.crossword.variables:
            self.domains[var] = {word for word in self.crossword.words if len(word) == var.length}

        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        xi, yi = self.crossword.overlaps[x, y] 

        if xi is None or yi is None:
            return False

        revised = False

        to_remove = set()
        for w1 in self.domains[x]:
            has_match = False
            for w2 in self.domains[y]:
                if w1 == w2:  # CROSSWORD SHOULD NOT CONTAIN SAME WORDS.
                    continue
                
                if w1[xi] == w2[yi]:
                    has_match = True
            
            if not has_match:  # IF NO MATCH IS FOUND IN SELF.DOMAIN[Y], REMOVE W1.
                to_remove.add(w1)
                        
        if to_remove:
            self.domains[x] -= to_remove
            revised = True

        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        """
        if arcs is None:
            queue = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        else:
            queue = arcs

        while queue:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in set(self.crossword.neighbors(x)) - {y}:
                    queue.append((z, x))
        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var, word in assignment.items():

            # Check unary constraints
            if len(word) != var.length:
                return False

            # Check conflicts with neighbors
            for neigh in self.crossword.neighbors(var):
                if neigh in assignment:
                    overlap = self.crossword.overlaps[var, neigh]
                    if overlap is not None:
                        xi, yi = overlap
                        if word[xi] != assignment[neigh][yi]:
                            return False

        # Check for duplicates
        if len(set(assignment.values())) != len(assignment.values()):
            return False

        return True



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # List of possible words for var (with matching length)
        words = [word for word in self.crossword.words if len(word) == len(var)]
        
        # Dictionary to count the number of conflicts for each word
        conflicts = {word: 0 for word in words}
        
        # Iterate over each neighbor of the variable var
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment:
                # Get the overlap position between var and its neighbor
                xi, yi = self.crossword.overlaps[var, neighbor]
                
                # Check how many words in the neighbor's domain are ruled out
                for word in words:
                    for w2 in self.crossword.words:
                        if len(w2) == len(neighbor) and word[xi] != w2[yi]:
                            conflicts[word] += 1
        
        # Sort words by the number of conflicts in ascending order
        sorted_words = sorted(conflicts, key=conflicts.get)
        
        return sorted_words

            

    def get_min_remaining_values_variable(self, assignment):
        min_remaining = int("inf")
        l = []
        for var in self.crossword.variables:
            if var not in assignment:
                domain_size = self.domains[var]
                if domain_size < min_remaining:
                    l = [var] 
                    min_remaining = len(self.domains[var])
                    
                elif len(self.domains[var]) == min_remaining:
                    l.append(var)
                    
        return l 
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_vars = self.get_min_remaining_values_variable(assignment)
        
        # IF THERE'S ONLY ONE VARIABLE WITH THE FEWEST VALES, RETURN IT. 
        if len(min_vars) == 1:
            return min_vars[0]
        
        # IF THERE IS A TIE, APPLY DEGREE HEURISTIC
        min_degree = -1
        selected_var = None
        for var in min_vars:
            neigh = self.crossword.neighbors(var)
            domain_size = len(neigh)
            if domain_size > min_degree:
                selected_var = var
                min_degree = domain_size
                
        return selected_var
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # IF THE ASSIGNMENT IS COMPLETE, RETURN IT
        if len(assignment) == len(self.crossword.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.domains[var]:
            copy_assignment = assignment.copy()
            copy_assignment[var] = value
            
            if self.consistent(copy_assignment):
                result = self.backtrack(copy_assignment)
                
                if result is not None:
                    return result
            
            del copy_assignment[var]
        
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
