import os
import numpy as np
import matplotlib.pyplot as plt
import time
from sudoku import Sudoku
from datetime import datetime
from pytz import timezone
import pytz
import cProfile
import subprocess

## Objective and procedure
# Sudoku game generator
# Generates both input and answer
#
# Last update: August 27, 2023
# Author: Jinwook Lee
#

class Input():
    # Input class
    def __init__(self):
        self.N_game = 10
        self.N_size = 9
        self.N_element = self.N_size**2
        self.N_seed = 2 # Seed to generate random game
        self.N_input_min = 20 # Count of provided numbers for problem
        self.N_input_max = 35 # Count of provided numbers for problem
        self.N_extract = 10 # Extract attempt limit
        
        self.n_guess_layer_list = range(0,6,2)
        self.n_trial_max = 500

def main_gen(out_dir,PDT_int):
    ## Input class
    INPUT = Input()

    ## Random game generator
    N_game = INPUT.N_game
    N_size = INPUT.N_size
    N_element = INPUT.N_element
    N_seed = INPUT.N_seed # Seed to generate random game
    N_input_min = INPUT.N_input_min
    N_input_max = INPUT.N_input_max
    N_extract = INPUT.N_extract
    n_guess_layer_list = INPUT.n_guess_layer_list
    n_trial_max = INPUT.n_trial_max

    n_game = 0
    while n_game < N_game:
        ## Random seed
        rand_array = []
        for n_row in range(N_size):
            cur_vect = np.arange(1,10)
            np.random.shuffle(cur_vect)
            rand_array.append(cur_vect.tolist())
        rand_vect = np.array(rand_array).flatten()
        i_select = np.random.choice(N_element,N_seed)
        
        zero_vect = np.zeros(N_size**2,dtype=int)
        zero_vect[i_select] = rand_vect[i_select]
        seed_mat = np.reshape(zero_vect,(N_size,N_size)).tolist()
        seed_game = Sudoku(seed_mat)
        seed_game.solve(N_size**2-N_seed,N_size**2,is_quiet=True)

        # Sanity check
        seed_game._scan()
        if seed_game.is_solved == False:
            continue
        else:
            print("\n\nFound a valid seed")
            seed_game.display()

            # Generate game
            seed_vect = np.array(seed_game.cur_mat).flatten()
            for n_extract in range(N_extract):
                print("\nExtracting attempt " + str(n_extract+1))
                N_input = np.random.randint(N_input_min,N_input_max)
                i_select = np.random.choice(N_element,N_input)
                zero_vect = np.zeros(N_size**2,dtype=int)
                zero_vect[i_select] = seed_vect[i_select]
                init_mat = np.reshape(zero_vect,(N_size,N_size)).tolist()
                cur_game = Sudoku(init_mat)
                cur_game.display()

                # Guess limit
                for n_guess_layer_max in n_guess_layer_list:
                    cur_game.N_trial = 0 # Reset trial count
                    cur_game.solve(n_guess_layer_max,n_trial_max,is_quiet=True)
                    if cur_game.is_solved == True:
                        break

                ## Display summary
                if cur_game.is_solved:
                    n_game += 1
                    print("\nSolved game " + str(n_game))
                    cur_game.display()

                    # Write
                    file_path = out_dir + "/PDT_" + str(PDT_int) + ".dat"
                    write_result(n_game,
                                N_input,
                                init_mat,
                                cur_game.cur_mat,
                                cur_game.N_layer_solved,
                                cur_game.N_trial,
                                file_path)
                    break
                else:
                    print("Failed to solve")

def write_result(n_game,N_input,input_mat,sol_mat,n_layer_solved,n_trial,file_path):
    ## Matrix size
    N_size = int(np.sqrt(np.size(input_mat)))
    N_block = int(np.sqrt(N_size))

    ## Open
    file = open(file_path,"a")

    ## Write
    # Header
    if n_game == 1: # No space for first case
        cur_str = ''
    else:
        cur_str = '\n\n\n'
    for n_col in range(2*N_size+2*N_block-2):
        cur_str += '*'
    file.write(cur_str)
    file.write("\n* Game: " + str(n_game))
    file.write("\n* Input count: " + str(N_input))
    cur_str = '\n'
    for n_col in range(2*N_size+2*N_block-2):
        cur_str += '*'
    file.write(cur_str)

    # Input/Output
    file.write("\n\n[Input]")
    write_mat2file(file,input_mat,N_size,N_block)
    file.write("\n\n[Output]")
    write_mat2file(file,sol_mat,N_size,N_block)

    # Solver info
    file.write("\n\n[Solver info]")
    file.write("\nLayer solved: " + str(n_layer_solved))
    file.write("\nTrial: " + str(n_trial))

    ## Close
    file.close()

def write_mat2file(file,cur_mat,N_size,N_block):
    # Conver to numpy array
    cur_mat = np.array(cur_mat)

    # Upper line
    cur_str = '\n'
    for n_col in range(2*N_size+2*N_block-2):
        cur_str += '='
    file.write(cur_str)

    # Main matrix
    for n_row in range(N_size):
        cur_str = '\n'
        for n_col in range(N_size):
            cur_val = cur_mat[n_row,n_col]
            if cur_val == 0:
                cur_str += '  '
            else:
                cur_str += str(cur_val) + ' '
            
            if (np.remainder(n_col+1,N_block) == 0) and (n_col+1 < N_size):
                cur_str += '| '
        file.write(cur_str)

        if (np.remainder(n_row+1,N_block) == 0) and (n_row+1 < N_size):
            cur_str = '\n'
            for n_col in range(2*N_size+2*N_block-2):
                cur_str += '-'
            file.write(cur_str)

    # Lower line
    cur_str = '\n'
    for n_col in range(2*N_size+2*N_block-2):
        cur_str += '='
    file.write(cur_str)

if __name__ == '__main__':
    ## Current PDT time
    date_format='%Y%m%d_%H%M'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    PDT_int = int(date.strftime(date_format))
    
    ## Time count
    t_start = time.perf_counter()

    ## Make directory
    out_dir = os.getcwd() + "/RandomGames"
    if os.path.exists(out_dir) == False:
        os.mkdir(out_dir)

    ## Main
    main_gen(out_dir,PDT_int)
    
    ## Elapsed time
    t_end = time.perf_counter()
    print("Elapsed time: {:.3f} seconds".format(t_end-t_start))

