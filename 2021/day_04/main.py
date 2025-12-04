"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (65325, 4624)


def score_board(grid, numbers, num_idx):
    return sum(val for row in grid for val in row if val not in numbers[:num_idx+1]) * numbers[num_idx]


@print_function
def main(input_txt: str) -> int:
    text_blocks = input_txt.split('\n\n')
    numbers = list(map(int, text_blocks.pop(0).split(',')))
    grids = [[list(map(int, re.findall('\\d+', line))) for line in grid.split('\n')] for grid in text_blocks]
    # Loop over all 'lines': each row and column of the grid. Find the line which completes the 
    # quickest. If the grid completes faster than any other, store it for p1 and if it is slower 
    # than any other, store it for p2.
    num_idx_p1 = len(numbers)
    num_idx_p2 = 0
    grid_p1 = None
    grid_p2 = None
    for grid in grids:
        grid_min_idx = len(numbers)
        lines = grid + [[row[col_idx] for row in grid] for col_idx in range(len(grid[0]))]
        for row in lines:
            line_min_idx = max(numbers.index(val) for val in row)
            if line_min_idx < grid_min_idx:
                grid_min_idx = line_min_idx
        if grid_min_idx > num_idx_p2:
            num_idx_p2 = grid_min_idx
            grid_p2 = grid
        if grid_min_idx < num_idx_p1:
            grid_p1 = grid
            num_idx_p1 = grid_min_idx
    # Score the boards
    score_p1 = 
    score_p2 = score_board(grid_p2, numbers, num_idx_p2)
    # Return
    return (score_p1, score_p2)


aoc_run( __name__, __file__, main, AOC_ANSWER)
