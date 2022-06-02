import os.path

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)

def first(iterable, default=None):
    """Return the first element of an iterable or the next element of a generator; or default."""
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


def open_data(name, mode='r'):
    aima_root = os.path.dirname(__file__)
    aima_file = os.path.join(aima_root, *['aima-data', name])

    return open(aima_file, mode=mode)

class CSP():
    def __init__(self, variables, domains, neighbors, constraints):
        self.constraints = constraints
        variables = variables or list(domains.keys())
        self.neighbors = neighbors
        self.domains = domains
        self.curr_domains = None
        self.nassigns = 0
        self.variables = variables
    def choices(self, var):
        """Return all available values for variable"""
        return (self.curr_domains or self.domains)[var]

    def nconflicts(self, var, val, assignment):
        """Return the count of conflicts between the given clique when assigned with the given value and the rest of cliques in the assignment."""
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    def goal_test(self, state):
        """check all variables has been assigned with the required constraint"""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def support_pruning(self):
        """Add variables to the current domain if it is empty"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def assign(self, var, val, assignment):
        """Add {var: val} to dictionary and delete the old value"""
        assignment[var] = val
        self.nassigns += 1
