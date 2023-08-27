import numpy as np
import matplotlib.pyplot as plt
import time
import cProfile
import subprocess

## Sudoku class
# All element positions have valid list of numbers
# Iteratively scan to update to reduce the valid list
# Tree search is then drilled down with random guess until invalidity is identified
#
# Last update: August 26, 2023
# Author: Jinwook Lee
#

class Sudoku():
    ## Class to control setup
    def __init__(self,init_mat,N_block=3):
        # Basic
        self.N_block = N_block # 3x3 is base block
        self.N_size = self.N_block**2 # 9x9 as default
        self.N_element = self.N_size**2 # 81 elements for default
        self.cur_mat = np.copy(init_mat) # np.zeros((N_size*N_size))
        self.N_guess_layer = 0 # Current layer of guess

        # Sanity check
        assert np.shape(init_mat) == (self.N_size,self.N_size)
        assert np.max(init_mat) <= 9
        assert np.max(init_mat) >= 0

        # Status flag
        self.is_valid = True
        self.is_solved = np.size(self.cur_mat[self.cur_mat==0]) == 0
        
        # List of valid numbers on each position
        self.val_list = np.ndarray((self.N_element),dtype=object)
        for n_element in range(self.N_element):
            n_row = int(n_element/self.N_size)
            n_col = np.remainder(n_element,self.N_size)
            cur_val = self.cur_mat[n_row,n_col]
            if cur_val != 0:
                # Single value if already solved
                self.val_list[n_element] = np.array([cur_val])
            else:
                # Full list if not solved
                self.val_list[n_element] = np.arange(self.N_size)+1 # e.g. 1, ..., 9

    def _copy_A2B(self,A,B):
        ## Copy A to B
        # Basic
        B.N_block = A.N_block
        B.N_size = A.N_size
        B.N_element = A.N_element
        B.cur_mat = A.cur_mat

        # Status flag
        B.is_valid = A.is_valid
        B.is_solved = A.is_solved
        B.val_list = A.val_list

    def _scan(self):
        # Min-max validity check
        if np.max(self.cur_mat) <= 9 and np.min(self.cur_mat) >= 0:
            # Flag initialization
            is_changed = False
            
            # Scan for each element
            for n_element in range(self.N_element):
                # Current coordinate
                n_row = int(n_element/self.N_size)
                n_col = np.remainder(n_element,self.N_size)
                cur_val = self.cur_mat[n_row,n_col]
                cur_val_list = self.val_list[n_element]
                
                n_block1 = int(n_row/self.N_block)
                n_block2 = int(n_col/self.N_block)
                
                # Pre-existing numbers
                n_row0 = n_block1*self.N_block
                n_col0 = n_block2*self.N_block
                n_rowE = n_row0 + self.N_block
                n_colE = n_col0 + self.N_block
                cur_block_list = self.cur_mat[n_row0:n_rowE,n_col0:n_colE].flatten()
                cur_row_list = self.cur_mat[n_row,:].flatten()
                cur_col_list = self.cur_mat[:,n_col].flatten()
                
                # Validity
                if cur_val == 0:
                    # Update validity list
                    cur_val_list = np.setdiff1d(cur_val_list, cur_block_list)
                    cur_val_list = np.setdiff1d(cur_val_list, cur_row_list)
                    cur_val_list = np.setdiff1d(cur_val_list, cur_col_list)
                    
                    if np.size(cur_val_list) != np.size(self.val_list[n_element]):
                        self.val_list[n_element] = cur_val_list

                        # Fill in matrix
                        if np.size(cur_val_list) == 1:
                            self.cur_mat[n_row,n_col] = cur_val_list[0]
                            is_changed = True
                        
                        # No more valid list
                        elif np.size(cur_val_list) == 0:
                            self.is_valid = False
                            break
                else:
                    i_block_match = cur_block_list == cur_val
                    i_row_match = cur_row_list == cur_val
                    i_col_match = cur_col_list == cur_val
                    if ((np.size(cur_block_list[i_block_match]) != 1) or
                       (np.size(cur_row_list[i_row_match]) != 1) or
                       (np.size(cur_col_list[i_col_match]) != 1)):
                        # Duplicate detected
                        self.is_valid = False
                        is_changed = False
                        break                
        else:
            self.is_valid = False
            is_changed = True

        # Solution status
        # - Check the count of zero is zero
        # - And matrix must be valid
        zero_count = np.size(self.cur_mat[self.cur_mat==0])
        self.is_solved = (zero_count == 0) and self.is_valid

        # End
        return is_changed
            
    def _random_guess(self):
        # Serach position with minimum element size
        is_found = False
        for cur_size in range(2,self.N_size+1):
            for n_element in range(self.N_element):
                if np.size(self.val_list[n_element]) == cur_size:
                    is_found = True
                    n_element_found = n_element
                    val_list_found = self.val_list[n_element]
                    break
            if is_found == True:
                break

        # Current coordinate
        n_row_found = int(n_element_found/self.N_size)
        n_col_found = np.remainder(n_element_found,self.N_size)

        # Pick
        val_pick = np.random.choice(val_list_found)
        
        # Generate new game with random guess
        R = Sudoku(self.cur_mat)
        R.cur_mat[n_row_found,n_col_found] = val_pick
        R.N_guess_layer = self.N_guess_layer + 1

        return R

    def solve(self):
        # Guess layer \t
        tStr = ""
        for _ in range(self.N_guess_layer):
            tStr += "\t"

        # Scan update until there is nothing more to change
        is_changed = self._scan()
        while (self.is_valid == True) and (is_changed == True):
            is_changed = self._scan()
        
        # Random guess if not solved
        # - This will be called recursively
        while self.is_solved == False:
            if self.is_valid == True:
                print(tStr + "Random Roll")
                R = self._random_guess()
                R.solve()
                if R.is_valid == False:
                    print(tStr + "Re-roll upstream")
                    R = self._random_guess()
                    R.solve()                
                if R.is_solved == True:
                    self._copy_A2B(R,self)
                    print(tStr + "Found solution")
                    break
            else: # self.is_valid == False:
                print(tStr + "Invalid guess")
                break

    def display(self):
        # Upper line
        cur_str = ''
        for n_col in range(2*self.N_size+2*self.N_block-2):
            cur_str += '='
        print(cur_str)

        # Main matrix
        for n_row in range(self.N_size):
            cur_str = ''
            for n_col in range(self.N_size):
                cur_val = self.cur_mat[n_row,n_col]
                if cur_val == 0:
                    cur_str += '  '
                else:
                    cur_str += str(cur_val) + ' '
                
                if (np.remainder(n_col+1,self.N_block) == 0) and (n_col+1 < self.N_size):
                    cur_str += '| '
            print(cur_str)

            if (np.remainder(n_row+1,self.N_block) == 0) and (n_row+1 < self.N_size):
                cur_str = ''
                for n_col in range(2*self.N_size+2*self.N_block-2):
                    cur_str += '-'
                print(cur_str)

        # Lower line
        cur_str = ''
        for n_col in range(2*self.N_size+2*self.N_block-2):
            cur_str += '='
        print(cur_str)