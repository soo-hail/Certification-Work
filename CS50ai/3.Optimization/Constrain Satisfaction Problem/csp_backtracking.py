VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]

CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]

def get_unassigned(assignments):
    """RETURNS THE VARIABLE THAT IS NOT YET ASSIGNED"""
    for var in VARIABLES:
        if var not in assignments:
            return var
    return None

def is_consistent(var, value, assignments):
    """CHECKS IF ASSIGNING `value` TO `var` IS CONSISTENT WITH CURRENT `assignments`"""
    for x, y in CONSTRAINTS:
        if (x == var and y in assignments and assignments[y] == value) or \
           (y == var and x in assignments and assignments[x] == value):
            return False
    return True

def backtrack(assignments):
    """BACKTRACKING ALGORITHM TO SOLVE THE EXAM SCHEDULING PROBLEM"""
    if len(assignments) == len(VARIABLES):  # All variables are assigned
        return assignments
    
    var = get_unassigned(assignments)
    
    for value in ["Monday", "Tuesday", "Wednesday"]:
        if is_consistent(var, value, assignments):
            assignments[var] = value  # Assign value to variable
            result = backtrack(assignments)  # Recursive call

            if result is not None:
                return result  # Solution found

            del assignments[var]  # Remove the variable assignment
    
    return None

# Example usage:
assignments = {}
result = backtrack(assignments)
print(result)
