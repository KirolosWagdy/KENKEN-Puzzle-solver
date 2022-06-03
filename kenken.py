from sqlalchemy import false, true
import csp
from sys import stderr
from itertools import product, permutations
from functools import reduce
from random import random, shuffle, randint, choice,randint
from time import time
from csv import writer
from generator import *


def in_bounds(members,s):
    member_not_in=[]
    for member in members:
        if member[0] < 1 or member[0] > s or member[1] < 1 or member[1] > s:
            member_not_in.append(member)
    return member_not_in
    
def check_board(size, cliques):
    """
    check the input board 
       For each clique
        1) Remove repeated members
        2)Validate the operator
        3)Check for clique members bounds
        4)Check if a member is common with other clique
       Check if all cliques cover the full board or not
    """
    mentioned = set()
    for i in range(len(cliques)):
        #(((1, 1), (1, 2)), '+', 11)
        members, operator, target = cliques[i]
        cliques[i] = (tuple(set(members)), operator, target)
        members, operator, target = cliques[i]
        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cliques[i], "is invalid", file=stderr)
            exit(1)
        violations = in_bounds(members,size)
        if violations:
            print("Members", violations, "of clique", cliques[i], "are out_csv of bounds", file=stderr)
            exit(2)
        violations = mentioned.intersection(set(members))
        if violations:
            print("Members", violations, "of clique", cliques[i], "are cross referenced", file=stderr)
            exit(3)
        mentioned.update(set(members))
    indexes = range(1, size + 1)
    violations = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)
    if violations:
        print("Positions", violations, "does not belong to any clique", file=stderr)
        exit(4)

def conflicting(A, a, B, b):
    for i in range(len(A)):
        for j in range(len(B)):
            # if at the same column or the same row and equal to each other
            if ((A[i][0] == B[j][0]) != (A[i][1] == B[j][1])) and a[i] == b[j]:
                return True
    return False

def valid_domains(domains,members,operator,target):
    """
    Return the valid domains for members
    """
    domains_element=[]
    for values in  domains[members]:
        for p in permutations(values):
            if reduce(operation(operator), p) == target:
                if not conflicting(members, values, members, values):
                    domains_element.append(values)
    return domains_element
def get_domains(size, cliques):
    """
    For every clique in cliques:
        1)Initialize the domain of each variable with all combinations of values from 1 -> board-size
        2)Discard any values that causes conflicts
    """
    domains = {}
    for clique in cliques:
        members, operator, target = clique
        # all possible domains
        domains[members] = list(product(range(1, size + 1), repeat=len(members)))
        # all valid domains
        domains[members] = valid_domains(domains,members,operator,target)
    return domains

def get_neighbors(cliques):
    """
    Determine the neighbors of each variable 
        For each clique 
         1)Start with empty list of neighbours
         2)For every clique other than the current one
            if they can cause conflict they are considered neighbors
    """
    neighbors = {}
    for members, _, _ in cliques:
        neighbors[members] = []
    for A, _, _ in cliques:
        for B, _, _ in cliques:
            if A != B and B not in neighbors[A]:
                #check if they are in the same row or the same column
                for i in range(len(A)):
                    for j in range(len(B)):
                        # add neighbors if at the same column or the same row and equal to each other
                        if ((A[i][0] == B[j][0]) != (A[i][1] == B[j][1])):
                            neighbors[A].append(B)
                            neighbors[B].append(A)
    return neighbors


class Kenken(csp.CSP):
    def __init__(self, size, cliques):
        """
        A clique example: (((x1, y1), ..., (xn, yn)), <operation>, <result>)
        """
        #Check that the board is valid
        check_board(size, cliques)
        variables=[]
        for clique1 in cliques:
            variables.append(clique1[0])
        domains = get_domains(size, cliques)
        neighbors = get_neighbors(cliques)
        print()
        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)
        self.size = size
        # Used in Perfomance_measureing
        self.checks = 0
        # Used in displaying
        self.padding = 0
        self.meta = {}
        for members, operator, target in cliques:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        
    def constraint(self, A, a, B, b):
        """
      Variables that share same row or column must not have the same value
        """
        self.checks += 1
        return A == B or not conflicting(A, a, B, b)


def main_algorithm(size, cliques,algorithm="BT"):
    """
    BT    -> Backtracking search
    BT+FC -> Backtracking search with Forward Checking
    BT+AC -> Backtracking search with Arc Consistency
    """
    ken = Kenken(size, cliques)
    if algorithm=="BT":
        assignment = csp.backtracking_search(ken)
    elif algorithm=="BT+FC":
        assignment = csp.backtracking_search(ken,inference=csp.forward_checking)
    elif algorithm=="BT+AC":
        assignment = csp.backtracking_search(ken,inference=csp.mac)
    else:
        print("unexpected algorithm")
    return assignment