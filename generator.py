from random import random, shuffle, randint, choice
from functools import reduce

def operation(operator):
   # from operator to string
   if operator == '+':
      return lambda a, b: a + b
   elif operator == '-':
      return lambda a, b: a - b
   elif operator == '*':
      return lambda a, b: a * b
   elif operator == '/':
      return lambda a, b: a / b
   else:
      return None

#check for adjacent coord
def adjacent(p1, p2):
   x1, y1 = p1
   x2, y2 = p2
   gx, gy = x1 - x2, y1 - y2
   return (gx == 0 and abs(gy) == 1) or (gy == 0 and abs(gx) == 1)

