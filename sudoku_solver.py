# Sudoku Solver
# by Walter Woshid

import os
import math
import time
import numpy as np
from termcolor import colored

# Clear interpreter output
def clear() -> None:
    # Windows / Linux
    os.system('cls' if os.name == 'nt' else 'clear')

# Define your sudoku here:
sudoku = np.concatenate([
    [5, 3, 0], [0, 7, 0], [0, 0, 0],
    [6, 0, 0], [1, 9, 5], [0, 0, 0],
    [0, 9, 8], [0, 0, 0], [0, 6, 0],

    [8, 0, 0], [0, 6, 0], [0, 0, 3],
    [4, 0, 0], [8, 0, 3], [0, 0, 1],
    [7, 0, 0], [0, 2, 0], [0, 0, 6],

    [0, 6, 0], [0, 0, 0], [2, 8, 0],
    [0, 0, 0], [4, 1, 9], [0, 0, 5],
    [0, 0, 0], [0, 8, 0], [0, 7, 9],
]).tolist()

# Prints the sudoku to the terminal
def print_sudoku(sudoku: list) -> None:

    def grey(str: str) -> str:
        return colored(str, color = 'grey')
    
    m_g = grey('-')
    l_g = grey('|')

    clear()
    print_statement = ''
    for x in range(len(sudoku) + 1):
        # Horizontal lines
        if (x % 27 == 0):
            print_statement += ('+' + ('-' * 3 + '+') * 9)

        # Break on last iteration
        if (x == len(sudoku)):
            break

        # New line after each row
        if (x % 9 == 0):
            print_statement += "\n"

        # Print lines between numbers
        if ((x % 9 == 0) & (x % 27 != 0)):
            print_statement += ('+' + (grey('-' * 3 + '+') * 2 + (m_g * 3 + '+')) * 3 + "\n")

        # Numbers with ' | ' in between
        number = str(sudoku[x])
        number = number if number != '0' else ' '
        print_statement += ('|' if (x % 3 == 0) else l_g) + ' ' + number + ' '

        # Last '|'
        if (x % 9 == 8):
            print_statement += '|'
        
        # New line
        if (x % 27 == 26):
            print_statement += "\n"
    print_statement += "\n"
    print(print_statement)

def get_row(sudoku: list, row: int) -> list:
    calc = math.floor(row / 9)
    result = sudoku[calc * 9:calc * 9 + 9]
    return [i for i in result if i != 0]

def get_column(sudoku: list, column: int) -> list:
    calc = column % 9
    result = sudoku[calc::9]
    return [i for i in result if i != 0]

def get_square(sudoku: list, index: int) -> list:
    horizontal = math.floor(index / 27) 
    vertical = math.floor((index % 9) / 3)
    nums = []
    for x in range(3):
        add = 3 * vertical
        fromI = (horizontal * 3 + x) * 9
        toI = fromI + 3
        nums.append(sudoku[fromI + add:toI + add])
    return np.concatenate(nums)

def get_available_combinations(sudoku: list, index: int) -> list:
    row = get_row(sudoku, index)
    column = get_column(sudoku, index)
    square = get_square(sudoku, index)
    return np.setdiff1d(range(1, 10), np.concatenate([row, column, square])).tolist()

def sudoku_is_valid(sudoku: list) -> bool:
    def has_duplicates(array: list) -> bool:
        return len(np.unique(array)) != len(array)

    for i in range(9):
        if (has_duplicates(get_row(sudoku, i))):
            return False
        if (has_duplicates(get_column(sudoku, i))):
            return False
        if (has_duplicates(get_row(sudoku, i))):
            return False
    
    return True

def solve_sudoku(sudoku: list) -> None:
    print('Solving sudoku. Please wait...')

    # Statistics
    start_time = time.time()
    steps = 0

    not_solvable_reason = 'Sudoku is not valid. Please check your sudoku and try again.'

    # Check if sudoku is valid
    if not sudoku_is_valid(sudoku):
        print(not_solvable_reason)
        return

    # Create a second sudoku to print to console
    visual_sudoku = sudoku[:]

    # {index => [possible combinations]}
    map = {}

    while (True):
        # Find zero
        try:
            index: int = sudoku.index(0)
        except ValueError:
            break

        # Get available combinations for that field
        if index in map:
            available = map[index]
        else:
            available = get_available_combinations(sudoku, index)

        # If no combinations
        if (len(available) == 0):
            lastIndex = list(map.keys())[-1]

            # Remove last number from grid
            sudoku[lastIndex] = 0
            visual_sudoku[lastIndex] = 0

            # Remove from list in map
            map[lastIndex].remove(map[lastIndex][0])

            # If last map empty
            while (len(map[lastIndex]) == 0):
                # Remove last map element
                del map[lastIndex]

                try:
                    lastIndex = list(map.keys())[-1]
                except IndexError:
                    print(not_solvable_reason)
                    return

                # Remove first element from prev map
                map[lastIndex].remove(map[lastIndex][0])

                # Remove from gird
                sudoku[lastIndex] = 0
                visual_sudoku[lastIndex] = 0

        else:
            # Add to map if it doesn't exist already
            if index not in map:
                map[index] = available

            # Place first number into sudoku
            sudoku[index] = available[0]
            visual_sudoku[index] = colored(available[0], color = 'green')

            steps += 1
    
    # Check again if sudoku is valid
    if not sudoku_is_valid(sudoku):
        print(not_solvable_reason)
    else:
        print_sudoku(visual_sudoku)
        print('Successfully solved sudoku in %s steps and %.2f seconds!' % (steps, time.time() - start_time), end = '\n\n')

solve_sudoku(sudoku)
