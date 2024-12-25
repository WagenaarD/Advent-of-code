"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""

AOC_ANSWER = (230, 9533698720)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import cache

@cache
def solve(input: str, step: tuple = (1, 3)):
    grid = input.split('\n')
    pos = 0, 0
    trees = 0
    while pos[0] < len(grid):
        trees += grid[pos[0]][pos[1]] == '#'
        pos = (pos[0] + step[0], (pos[1] + step[1]) % len(grid[0]))
    return trees

@print_function
def part_one(input: str) -> int:
    return solve(input, (1, 3))

@print_function
def part_two(input: str) -> int:
    # Part 2
    # Right 1, down 1.
    # Right 3, down 1. (This is the slope you already checked.)
    # Right 5, down 1.
    # Right 7, down 1.
    # Right 1, down 2.
    p2 = 1
    for step in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        p2 *= solve(input, step)
    return p2

@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


