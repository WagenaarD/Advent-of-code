"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in

New attempt to try a non-Z3 solution.
Takes 0.3s in pypy, 2.4s in python when verbose is False
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import deque
from pprint import pformat
from fractions import Fraction
import itertools as it
import math

AOC_ANSWER = (530, 20172)


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    score_p1 = 0
    for line in lines:
        # Parse input
        parts = line.split(' ')
        diagram = parts[0][1:-1]
        diagram = tuple(char == '#' for char in diagram)
        buttons = [list(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        # joltage = tuple(map(int, parts[-1][1:-1].split(',')))
        # Broad-first-search (BFS) over which buttons to press untill we find one leading to the 
        # correct machine settings
        start = (False, ) * len(diagram)
        stack = deque([(0, start)])
        seen = set()
        while True:
            steps, pos = stack.popleft()
            if diagram == pos:
                score_p1 += steps
                break
            if pos in seen:
                continue
            seen.add(pos)
            for button in buttons:
                new_pos = tuple(p != (idx in button) for idx, p in enumerate(pos))
                stack.append((steps + 1, new_pos))
    return score_p1


def get_row_echelon_form(matrix: list[list[Fraction]], verbose = True) -> tuple[list[int], list[list[Fraction]]]:
    free_variables = []
    selected_row_idx, processed_rows = 0, 0
    for col_idx in range(len(matrix[0]) - 1):
        if verbose:
            print_matrix(matrix)
            print(f'{processed_rows=} {free_variables=}, {col_idx=}')
        # Take any row that has a value for col_idx
        for row_idx in range(processed_rows, len(matrix)):
            if matrix[row_idx][col_idx]:
                selected_row_idx = row_idx
                if verbose:
                    print(f'{selected_row_idx=} for {col_idx=}')
                break
        else:
            free_variables.append(col_idx)
            continue
        # Normalize the row to have a 1
        matrix[selected_row_idx] = [val / matrix[selected_row_idx][col_idx] for val in matrix[selected_row_idx]]
        # Use this row to set the rest of the column to zero
        for row_idx, row in enumerate(matrix):
            if row_idx == selected_row_idx or row[col_idx] == 0:
                continue
            matrix[row_idx] = [row[c] - matrix[selected_row_idx][c] * row[col_idx] for c in range(len(row))]
        # Put that row on top
        matrix[processed_rows], matrix[selected_row_idx] = matrix[selected_row_idx], matrix[processed_rows]
        processed_rows += 1
    if verbose:
        print(f'Final row-echelon-form matrix')
        print(f'{free_variables=}')
        print_matrix(matrix)
    return (free_variables, matrix)


def print_matrix(matrix: list[list[Fraction]]):
    """
    Makes a 'pretty' print of the matrix notation of the problem. Fractions are displayed as ints if
    possible and otherwise as a fraction (e.g., Fraction(3, 2) becomes 3/2).
    """
    stringified_matrix = [
        [str(val) if int(val)==val else f'{val.numerator}/{val.denominator}' for val in row] 
        for row in matrix
    ]
    print(pformat(stringified_matrix, width=120).replace("'", ''))


@print_function
def part_two(input_txt: str, verbose: bool = True) -> int:
    """
    Solved with Z3 arithmatic solver. I hate it with a passion, but it is very strong and 
    surprisingly fast.

    Z3 defines a set of algebraic equations which it solves algebraically. 
    """
    lines = input_txt.split('\n')
    score_p2 = 0
    for line in lines:
        
        # Parse input
        parts = line.split(' ')
        buttons = [list(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        joltage = tuple(map(int, parts[-1][1:-1].split(',')))
        # construct matrix of linear equations. Each column represents one button, each row one 
        # joltage requirement with the last cell being the joltage values
        matrix = [
            [Fraction(jolt_idx in button, 1) for button in buttons] + [Fraction(jolt, 1)] 
            for jolt_idx, jolt in enumerate(joltage)
        ]
        if verbose:
            print(f'{lines.index(line)=}; {line=}')
        # convert to row echelon form (REF) and identify free_variables
        free_variables, matrix = get_row_echelon_form(matrix, verbose)
        # Loop over all values for the free variables
        fewest_presses = sum(joltage) + 1
        # Pre-calculate the maximum value of each individual free variable. The number of presses on
        # each free variable can never exceed that of the lowest joltage requirement of any of the 
        # joltages that it activates. This speeds up calculation time massively (70s to 11s)
        max_free_values = []
        for col_idx in free_variables:
            max_values = [min(joltage[button] for button in buttons[col_idx])]
            # If a row in the row-epsilon-form matrix is all-positive and contains a positive 
            # value for our free variable, the free variable cannot be soo high to exceed the 
            # joltage requirement
            for row in matrix:
                if row[col_idx] <= 0 or not all(r >= 0 for r in row[:-1]):
                    continue
                max_values.append(row[-1]//row[col_idx])
            max_value = min(max_values)
            max_free_values.append(range(max_value + 1))
            if verbose:
                print(f'Button {col_idx} can have any value in the range [0-{max_value}]')
        if verbose:
            print(f'Iterating over {math.prod(max(rng) for rng in max_free_values)} solutions to find '\
                  'fewest presses')
        for free_values in it.product(*max_free_values):
            # Count the number of keypresses of the free variables
            solution_presses = sum(free_values)
            # Add the keypresses of buttons bound to a joltage requirement (=row)
            for row in matrix:
                # Each row only has values at positions of one button and the free variables. 
                # Calculate how often those buttons need to be pressed
                row_presses = row[-1]
                for free_col, free_val in zip(free_variables, free_values):
                    row_presses -= row[free_col] * free_val
                if row_presses < 0 or int(row_presses) != row_presses:
                    break
                solution_presses += int(row_presses)
                if solution_presses >= fewest_presses:
                    break
            else:
                fewest_presses = solution_presses
        score_p2 += fewest_presses
    return score_p2



@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

# aoc_run( __name__, __file__, main, (7, 33), 'ex')
aoc_run( __name__, __file__, main, AOC_ANSWER)
