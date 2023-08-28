import itertools
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
        self.N_trial = 0 # Current trial counter
        self.N_layer_solved = 0 # Layer at solution

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
        B.N_block = np.copy(A.N_block)
        B.N_size = np.copy(A.N_size)
        B.N_element = np.copy(A.N_element)
        B.cur_mat = np.copy(A.cur_mat)

        # Status flag
        B.is_valid = np.copy(A.is_valid)
        B.is_solved = np.copy(A.is_solved)
        B.val_list = np.copy(A.val_list)

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
                cur_pre_list = np.concatenate((cur_block_list,
                                               cur_row_list,
                                               cur_col_list))
                cur_pre_uniq = np.unique(cur_pre_list)
                
                # Validity
                if cur_val == 0:
                    # Update validity list
                    cur_val_list = np.setdiff1d(cur_val_list, cur_pre_uniq, assume_unique=True)
                    
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
    
    def _sort_val_list_size(self):
        # Sorted list of element position
        # based on size of val_list

        # Array of val_list size
        val_list_size = np.zeros(self.N_element)
        for n_element in range(self.N_element):
            val_list_size[n_element] = np.size(self.val_list[n_element])

        # Sorted list
        n_element_list = np.argsort(val_list_size)
        return n_element_list

    def _replaced_game(self,n_element,val):
        n_row = int(n_element/self.N_size)
        n_col = np.remainder(n_element,self.N_size)
        
        R = Sudoku(self.cur_mat)
        R.cur_mat[n_row,n_col] = val
        R.N_guess_layer = self.N_guess_layer + 1
        R.N_trial = self.N_trial + 1
        
        return R
        
    def solve(self,n_guess_layer_max,n_trial_max,is_quiet=False):
        ## Recurvise solver
        # This method has critical issue to duplicate survey

        # Guess layer \t
        tStr = ""
        for _ in range(self.N_guess_layer):
            tStr += "."
        
        # Scan update until there is nothing more to change
        self._scan_till_end()
        
        # Drill down if valid but not solved
        # - This will be called recursively
        if ((self.N_guess_layer < n_guess_layer_max) and  # Guess Layer
            (self.is_valid == True) and # Validity
            (self.is_solved == False)): # Solved status
            for n_element_fill in self._sort_val_list_size():
                if np.size(self.val_list[n_element_fill]) == 1:
                    continue
                else:
                    val_list_fill = self.val_list[n_element_fill]
                    for val in val_list_fill:
                        # Trial limit check
                        if np.remainder(self.N_trial,100)==0:
                            if is_quiet == False:
                                print(tStr + "Current trial: " + str(self.N_trial))
                        if self.N_trial  > n_trial_max:
                            #print(tStr + "Exceeded trial limit")
                            return
                        
                        #n_row_fill = int(n_element_fill/self.N_size)
                        #n_col_fill = np.remainder(n_element_fill,self.N_size)
                        #print(tStr + "Guess: (" + str(n_row_fill) + ", " + str(n_col_fill) + ") = " + str(val))
                        R = self._replaced_game(n_element_fill,val)
                        R.solve(n_guess_layer_max,n_trial_max,is_quiet)
                        self.N_trial = R.N_trial
                        if R.is_valid == False:
                            continue           
                        if R.is_solved == True:
                            self._copy_A2B(R,self)
                            if R.N_layer_solved != 0:
                                # Roll upstream
                                self.N_layer_solved = R.N_layer_solved
                            else: # First encounter
                                self.N_layer_solved = R.N_guess_layer
                            if is_quiet == False:
                                print(tStr + "Found solution at trial " + str(self.N_trial))
                            break
                    #if self.N_trial  > n_trial_max:
                    #    print(tStr + "Exceeded trial limit")
                    #    return
                if (self.is_solved == True):
                    break

    def _scan_till_end(self):
        # Call scan until change stops or invalidated
        is_changed = self._scan()
        while (self.is_valid == True) and (is_changed == True):
            is_changed = self._scan()

    def _extract_candidates(self,N_extract):
        ## Extract combination of element
        # - In order of val_list size
        # - Using itertools.combinations(p,q)
        # - Outputs list of tuples of selected n_element

        # Array of val_list size
        val_list_size = np.zeros(self.N_element)
        for n_element in range(self.N_element):
            val_list_size[n_element] = np.size(self.val_list[n_element])

        # Sorted list
        val_list_size_sorted = np.sort(val_list_size)
        n_element_list_sorted = np.argsort(val_list_size)

        # Ignore single size (determined) elements
        i_unity = val_list_size_sorted == 1
        n_element_list_sel = n_element_list_sorted[np.invert(i_unity)]

        # Return combinatoric output in list of tuples
        return list(itertools.combinations(n_element_list_sel,N_extract))

    def solve_comb(self,N_guess,n_trial_max,is_quiet=False):
        ## Combinatoric solver
        # - Survey of combinatoric candidate lists for a given guess layer
        # - Cutoff once trial_max is reached
        
        # Scan update until there is nothing more to change
        self._scan_till_end()

        # Exit if done
        # Save current case for iteration
        if ((self.is_valid == False) or # Invalid or
            (self.is_solved == True)): # Solved
            return
        else:
            init_game = Sudoku(self.cur_mat)

        ## Start to guess if valid but not solved
        # Candidate pairs
        #n_element_tuple_list = self._extract_candidates(N_guess)
        #N_tuple = len(n_element_tuple_list)
        #for n_tuple in range(N_tuple):
        #    n_element_tuple = n_element_tuple_list[n_tuple]
        for n_element_tuple in self._extract_candidates(N_guess):        
            # Iteration size
            N_iter = 1
            val_list_size = np.zeros(N_guess,dtype=int)
            for n_guess in range(N_guess):
                val_list_size[n_guess] = np.size(self.val_list[n_element_tuple[n_guess]])
                N_iter *= val_list_size[n_guess]

            # Iteration
            for n_iter in range(N_iter):
                # Update trial count
                self.N_trial +=  1

                # Index position
                if n_iter == 0:
                    index_pos = np.zeros(N_guess,dtype=int)
                else:
                    # Click-up
                    index_pos[0] += 1

                    # Carry
                    for n_guess in range(N_guess):
                        if index_pos[n_guess] >= val_list_size[n_guess]:
                            index_pos[n_guess] = 0
                            if n_guess < N_guess-1:
                                index_pos[n_guess+1] += 1
                
                # Matrix update
                for n_guess in range(N_guess):
                    n_element = n_element_tuple[n_guess]
                    n_row = int(n_element/self.N_size)
                    n_col = np.remainder(n_element,self.N_size)
                    val = self.val_list[n_element][index_pos[n_guess]]
                    self.cur_mat[n_row,n_col] = val
                #print(str(n_element_tuple) + " " + str(index_pos))
                
                # Scan till end
                self._scan_till_end()

                # Exit if solved
                # Reset if not
                if self.is_solved == True:
                    return
                else:
                    self._copy_A2B(init_game,self)

                # Trial limit check
                if np.remainder(self.N_trial,100)==0:
                    if is_quiet == False:
                        print("Current trial: " + str(self.N_trial))
                if self.N_trial > n_trial_max:
                    #print(tStr + "Exceeded trial limit")
                    return
        
        print("Ended survey without solving")

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