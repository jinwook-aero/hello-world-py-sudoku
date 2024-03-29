import numpy as np

def example(n_case):
    # https://www.7sudoku.com/print_puzzles
    # MonthlySudokuPuzzlePack202306.pdf
    if n_case == 0:
        init_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    elif n_case == 1: # Difficulty I
        init_array = [[1, 0, 0, 0, 0, 0, 8, 3, 0],
                      [0, 0, 0, 3, 5, 0, 0, 2, 0],
                      [0, 2, 0, 0, 0, 7, 0, 4, 0],
                      [8, 0, 0, 0, 0, 2, 5, 1, 0],
                      [0, 0, 7, 1, 0, 5, 3, 0, 0],
                      [0, 9, 1, 7, 0, 0, 0, 0, 2],
                      [0, 5, 0, 9, 0, 0, 0, 8, 0],
                      [0, 1, 0, 0, 7, 3, 0, 0, 0],
                      [0, 4, 9, 0, 0, 0, 0, 0, 6]]
    elif n_case == 7: # Difficulty II
        init_array = [[0, 0, 9, 0, 8, 0, 0, 0, 0],
                      [8, 0, 0, 0, 9, 0, 0, 3, 2],
                      [0, 0, 0, 0, 6, 4, 0, 0, 9],
                      [2, 0, 1, 0, 0, 8, 0, 0, 0],
                      [0, 5, 0, 0, 3, 0, 0, 8, 0],
                      [0, 0, 0, 2, 0, 0, 6, 0, 3],
                      [9, 0, 0, 4, 2, 0, 0, 0, 0],
                      [3, 8, 0, 0, 7, 0, 0, 0, 1],
                      [0, 0, 0, 0, 1, 0, 7, 0, 0]]
    elif n_case == 13: # Difficulty III
        init_array = [[5, 0, 3, 0, 0, 0, 0, 0, 0],
                      [0, 0, 7, 9, 3, 2, 0, 0, 0],
                      [6, 0, 8, 0, 0, 0, 2, 0, 0],
                      [0, 7, 0, 0, 1, 4, 0, 5, 0],
                      [0, 0, 6, 0, 7, 0, 3, 0, 0],
                      [0, 5, 0, 2, 9, 0, 0, 7, 0],
                      [0, 0, 5, 0, 0, 0, 7, 0, 9],
                      [0, 0, 0, 7, 6, 9, 5, 0, 0],
                      [0, 0, 0, 0, 0, 0, 4, 0, 1]]
    elif n_case == 19: # Difficulty IV
        init_array = [[0, 2, 0, 0, 5, 9, 0, 0, 3],
                      [9, 3, 0, 1, 0, 0, 0, 0, 6],
                      [0, 5, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 5, 0, 3, 8, 0, 0],
                      [0, 0, 7, 0, 0, 0, 6, 0, 0],
                      [0, 0, 5, 2, 0, 8, 4, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 8, 0],
                      [4, 0, 0, 0, 0, 5, 0, 9, 7],
                      [8, 0, 0, 9, 2, 0, 0, 6, 0]]
    elif n_case == 25: #Difficulty V
        init_array = [[2, 0, 0, 0, 0, 7, 0, 0, 0],
                      [6, 3, 0, 0, 0, 9, 0, 0, 0],
                      [0, 0, 0, 6, 1, 0, 4, 0, 0],
                      [0, 0, 8, 4, 0, 2, 0, 0, 6],
                      [0, 0, 6, 0, 0, 0, 2, 0, 0],
                      [4, 0, 0, 9, 0, 6, 5, 0, 0],
                      [0, 0, 5, 0, 2, 8, 0, 0, 0],
                      [0, 0, 0, 5, 0, 0, 0, 9, 1],
                      [0, 0, 0, 1, 0, 0, 0, 0, 5]]
    else:
        init_array = np.rand((9,9))

    return init_array


    """
    elif n_case == 99:
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