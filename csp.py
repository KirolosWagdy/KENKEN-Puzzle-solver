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

    def unassign(self, var, assignment):
        """Delete {var: val} from dictionary"""
        if var in assignment:
            del assignment[var]

    def prune(self, var, value, removals):
        """prune some value from variables"""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):
        """return the removed variables to the current domains"""
        for B, b in removals:
            self.curr_domains[B].append(b)

def Remove_inconsistent_values(csp, Xi, Xj, removals):
    """Return true if all values not valid for the constraints"""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def first_unassigned_variable(assignment, csp):
    """Return the first variable"""
    var=[]
    for var1 in csp.variables:
        if var1 not in assignment:
            var.append(var1)
    return first(var)

def unordered_domain_values(var, assignment, csp):
    """Retuen the default order order of value"""
    return csp.choices(var)

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    """Remove neighbor values that don't satisfy the constraints"""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True

def mac(csp, var, value, assignment, removals):
    """for arc consistency"""
    queue=[]
    for neighbor in csp.neighbors[var]:
        queue.append((neighbor, var))
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if Remove_inconsistent_values(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result