from kenken import *
import sys
input=sys.argv
lower_limit=int(input[1])
upper_limit=int(input[2])
def Perfomance_measure(kenken, algorithm):
        """
        To measure the perfomance of the given algorithm from the following points:
          1)The number of visited nodes
          2)The number of constraints checking
          3)The number of done assignments 
          4)the run time
        """
        kenken.checks = kenken.nassigns = 0
        dt = time()
        assignment = algorithm(kenken)
        dt = time() - dt
        return assignment, (kenken.checks, kenken.nassigns, dt)

def results_generator(i, out_csv):
    """
    Perfomance_measure each one of the following algorithms for various kenken puzzles

       For each algorithm
         For all board sizes
          1)Create random kenken puzzles of the current size.
          2)Test the algorithm using the generated board
        Save the results into a csv file
    """
    bt         = lambda ken: csp.backtracking_search(ken)
    fc         = lambda ken: csp.backtracking_search(ken, inference=csp.forward_checking)
    mac        = lambda ken: csp.backtracking_search(ken, inference=csp.mac)
    algorithms = {
        "BT": bt, 
        "BT+FC": fc,
        "BT+AC": mac,
    }
    with open(out_csv, "w+") as file:
        out_csv = writer(file)
        out_csv.writerow(["Algorithm", "Size", "Constraint checks", "Assignments", "Completion time"])
        for i in range(1,101):
            size=randint(lower_limit,upper_limit)
            cliques = generate_board(size)
            for name, algorithm in algorithms.items():
                
                checks, assignments, dt = (0, 0, 0)
                assignment, data_out = Perfomance_measure(Kenken(size, cliques), algorithm)
                print("algorithm =",  name, "size =", size, "iteration =", i, "result =", "Success" if assignment else "Failure", file=stderr)
                checks      += data_out[0] / i
                assignments += data_out[1] / i
                dt          += data_out[2] / i
                out_csv.writerow([name, size, checks, assignments, dt])
    
x="result.csv"
results_generator(1,x)