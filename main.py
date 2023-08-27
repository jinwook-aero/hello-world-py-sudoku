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
# Last update: August 27, 2023
# Author: Jinwook Lee
#

def main(profileName):
    ## Initialize
    init_array = example(7) # 1, 7, 13, 25
    init_mat = np.array(init_array)

    cur_game = Sudoku(init_mat)
    print("Input matrix")
    cur_game.display()

    ## Start solver
    print("\nSolver started")
    profiler = cProfile.Profile()
    profiler.enable()
    for n_guess_limit in range(5):
        cur_game.solve(n_guess_limit)
        if cur_game.is_solved:
            break
    
    ## Dump profiling
    profiler.disable()
    profiler.dump_stats(profileName)

    ## Display summary
    if cur_game.is_solved:
        print("\nSolved matrix")
        cur_game.display()
    else:
        print("\nFailed to solve")

if __name__ == '__main__':
    ## Profiling main
    t_start = time.perf_counter()
    profileName = 'temp.prof'
    main(profileName)
    
    ## Elapsed time
    t_end = time.perf_counter()
    print("Elapsed time: {:.3f} seconds".format(t_end-t_start))

    ## Profiling visualization
    snakeVizCmd = "python -m snakeviz " + profileName
    removeCmd_dos = "del " + profileName
    removeCmd_linux = "rm " + profileName
    p = subprocess.Popen(snakeVizCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    userInput = input("Enter to complete")
    p = subprocess.Popen(removeCmd_dos, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p = subprocess.Popen(removeCmd_linux, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    ## End
    t_end = time.perf_counter()
    print("Elapsed time: {:.3f} seconds".format(t_end-t_start))

