"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (814, 924)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache
import math
from pprint import pprint

ADJ8 = [(x, y) for x, y in it.product([-1, 0, 1], repeat=2) if not (x, y) == (0, 0)]

def update_grid(grid: list[list[bool]]) -> list[list[bool]]:
    ngrid = [[False for char in row] for row in grid]
    # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            # neighbours = sum()
            neighbours = 0
            for dr, dc in ADJ8:
                if row+dr in range(rows) and col+dc in range(cols):
                    if grid[row+dr][col+dc]:
                        neighbours += 1
            if grid[row][col]:
                ngrid[row][col] = neighbours in [2, 3]
            else:
                ngrid[row][col] = neighbours == 3
    
    return ngrid


def set_corners(grid: list[list[bool]]) -> list[list[bool]]:
    for row, col in it.product([0, -1], repeat=2):
        grid[row][col] = True
    return grid


def print_grid(grid) -> None:
    print('\n'.join([''.join(['#' if char else '.' for char in row]) for row in grid]))


@print_function
def solve(grid: list[list[bool]], force_corners: bool, iterations: int, do_print: bool) -> int:
    if force_corners:
        grid = set_corners(grid)
    if do_print:
        print_grid(grid)
    for idx in range(iterations):
        grid = update_grid(grid)
        if force_corners:
            grid = set_corners(grid)
        if do_print:
            print(f'\nAfter {idx+1} steps:')
            print_grid(grid)
    return sum(sum(row) for row in grid)

@print_function
def main(input: str) -> tuple[int, int]:
    grid = [[char == '#' for char in row] for row in input.split('\n')]
    iterations = 100 if len(grid) > 6 else 4
    do_print = len(grid) == 6
    return (
        solve(grid, False, iterations, do_print), 
        solve(grid, True, iterations, do_print),
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


