"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict

AOC_ANSWER = (1393, 8643)


@print_function
def main(input_txt: str) -> int:
    # Store input as a list of coordinates. Coordinates stored in (row, column) format
    lines = input_txt.split('\n')
    rolls = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '@':
                rolls.append((row, col))
    
    score_p1 = None
    number_of_rolls_at_start = len(rolls)
    old_len = number_of_rolls_at_start + 1
    while len(rolls) < old_len:
        # Score neighbours from interaction-point-of-view: For each coordinate, increment the 
        # neighbour_count of surrounding positions (even if they contain no roll)
        neighbours = defaultdict(int)
        for row, col in rolls:
            for drow, dcol in it.product((-1, 0, 1), repeat=2):
                npos = (row + drow, col + dcol)
                neighbours[npos] += 1
            neighbours[(row, col)] -= 1
        # After the first round, score the number of rolls removed
        if score_p1 is None:
            score_p1 = sum(1 for pos in rolls if neighbours[pos] < 4)
        # Update roll positions
        old_len = len(rolls)
        rolls = [pos for pos in rolls if neighbours[pos] >= 4]
    # Score of p2 is the initial amount of rolls - the remaining rolls
    score_p2 = number_of_rolls_at_start - len(rolls)
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
