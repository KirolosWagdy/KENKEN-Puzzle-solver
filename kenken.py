from sqlalchemy import false, true
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
