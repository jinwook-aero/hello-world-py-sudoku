import numpy as np
import matplotlib.pyplot as plt
import time
from sudoku import Sudoku
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
    # Zeros
    """
    init_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """

    # Ex1
    init_array = [[1, 0, 0, 3, 9, 0, 8, 0, 0],
                  [5, 0, 0, 0, 6, 0, 0, 9, 0],
                  [0, 0, 2, 8, 0, 0, 4, 6, 0],
                  [0, 0, 3, 9, 0, 7, 0, 4, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 6, 0, 4, 5, 0, 0],
                  [0, 3, 6, 0, 0, 9, 7, 0, 0],
                  [0, 5, 0, 0, 3, 0, 0, 0, 4],
                  [0, 0, 8, 0, 4, 6, 0, 0, 5]]

    # Ex2
    """
    init_array = [[0, 0, 9, 0, 3, 8, 0, 7, 4],
                  [5, 0, 0, 0, 0, 0, 0, 8, 0],
                  [0, 0, 0, 0, 6, 7, 0, 0, 0],
                  [0, 9, 7, 8, 0, 0, 6, 0, 0],
                  [0, 0, 2, 0, 0, 0, 4, 0, 0],
                  [0, 0, 5, 0, 0, 6, 1, 9, 0],
                  [0, 0, 0, 6, 2, 0, 0, 0, 0],
                  [0, 2, 0, 0, 0, 0, 0, 0, 9],
                  [9, 3, 0, 4, 8, 0, 7, 0, 0]]
    """
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
