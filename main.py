import numpy as np
import matplotlib.pyplot as plt
import time
from sudoku import Sudoku
from example import example
import cProfile
import subprocess

## Objective and procedure
# Set and solve Sudoku
#
# Last update: August 26, 2023
# Author: Jinwook Lee
#

def main():
    ## Initialize
    init_array = example(13) # 1, 7, 13, 25
    init_mat = np.array(init_array)

    cur_game = Sudoku(init_mat)
    print("Input matrix")
    cur_game.display()

    print("\nSolver started")
    cur_game.solve()
    
    if cur_game.is_solved:
        print("\nSolved matrix")
        cur_game.display()
    else:
        print("\nFailed to solve")

if __name__ == '__main__':
    ## Profiling main
    t_start = time.perf_counter()
    main()      

    ## End
    t_end = time.perf_counter()
    print("Elapsed time: {:.3f} seconds".format(t_end-t_start))
