class Variable(): # TO REPRESENT A VARIBALE IN CROSSWORD(PUZZLE)

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length): # VARIBALE IS DEFINED BASED ON 4 PARAMETERS(ROW, COL, DIRECTION, LENGTH)
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = [] # CELLS BELONGS TO VARIBLE.
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0), # ROW("I") WILL CHANGE ONLY WHEN DIRECTION OF VARIBALE IS "DOWN"
                 self.j + (k if self.direction == Variable.ACROSS else 0)) # COL("J") WILL CHANGE ONLY WHEN DIRECTION OF VARIBALE IS "ACROSS"
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():

    def __init__(self, structure_file, words_file):

        # Determine structure of crossword
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []
            for i in range(self.height):
                row = []
                # TRUE ---> EMPTY-CELL, FALSE ---> CAN'T PLACE A LETTER
                for j in range(self.width):
                    if j >= len(contents[i]): # IF LENGTH OF LINE IS LESS THAN LENGTH OF MAX-WIDTH LINE.
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)

        # Save vocabulary list
        with open(words_file) as f:
            self.words = set(f.read().upper().splitlines())

        # Determine variable set
        self.variables = set()
        for i in range(self.height): # TRAVERSING THE PUZZLE.
            for j in range(self.width):

                # Vertical words
                starts_word = ( # START CELL(INDEX) OF A VERTICAL-WORD.
                    self.structure[i][j]
                    and (i == 0 or not self.structure[i - 1][j]) # CONSTRAIN FOR A CELL TO BE START-CELL OF A "VERTICAL VARIABLE"
                )
                if starts_word:
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Horizontal words
                starts_word = ( # START CELL(INDEX) OF A HORIZONTAL-WORD.
                    self.structure[i][j]
                    and (j == 0 or not self.structure[i][j - 1]) # CONSTRAIN FOR A CELL TO BE START-CELL OF A "HORIZONTAL VARIBALE"
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.ACROSS,
                            length=length
                        ))

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2: # GOT SAME VARIABLE.
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection: # CAN'T STORE LETTER(CELL == FALSE)
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var] # IGNORE ITSELF AND RETURN NEIGHBOURS(IF THEY HAVE OVERLAPPING CELLS MEANS THEY ARE NEIGHBOURS).
        )
