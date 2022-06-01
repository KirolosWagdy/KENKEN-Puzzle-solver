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


def generate_board(size):
   # put numbers in board statisfying the constrains (rows, columns)
   l=[]
   board=[]
   for i in range(size):
      for j in range(size):
         l.append(((i + j) % size) + 1)
      board.append(l)
      l=[]

   shuffle(board)  # row shuffle
   
   for c1 in range(size):  # column shuffle
      for c2 in range(size):
         if random() > 0.5:
               for r in range(size):
                  board[r][c1], board[r][c2] = board[r][c2], board[r][c1]
   # dictionary { coord: num }
   board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}
   # board coordinates sorting by columns
   uncaged = sorted(board.keys(), key=lambda var: var[1])

   cage = []
   while uncaged:
      #empty cage
      cage.append([])
      #choose random cage size
      cage_size = randint(1, 4)
      #take first element that is still uncaged
      cell = uncaged[0]
      #remove this element from the uncaged
      uncaged.remove(cell)
      #put this element as a first one in the cage
      cage[-1].append(cell)
      #loop untill occupy all elemnts in the cage
      i=0
      while i < cage_size - 1:
         #check for cell adjacents 
         adjecents = []
         for var in uncaged:
               if adjacent(cell, var):  # true/false
                  adjecents.append(var)

         adj=[]
         for one in uncaged:
             if adjacent(cell,one): #check for adjancy
                 adj.append(one)
         #random choice for the adjacents 
         cell = choice(adj) if adj else None
         if not cell:
            break
         #if chosen to be in this cage it is removed from the uncaged and added to the cage
         uncaged.remove(cell)
         cage[-1].append(cell)
         i+=1
      i=0
      #choose the opration 
      cage_size = len(cage[-1])
      if cage_size == 1:
         cell = cage[-1][0]
         cage[-1] = ((cell,), '.', board[cell])
         continue
      elif cage_size == 2:
         if board[cage[-1][0]] / board[cage[-1][1]] > 0 and not board[cage[-1][0]] % board[cage[-1][1]]:
            operator = "/"
         else:
            operator = "-"
      else:
         operator = choice("+*")
      #get target value 
      value = reduce(operation(operator), [board[cell] for cell in cage[-1]])
      #prepare the tuples 
      cage[-1] = (tuple(cage[-1]), operator, int(value))
   return cage

