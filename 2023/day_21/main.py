"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (None, None)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math



"""
S   Start (also garden plot)
.   Garden plots
#   Rocks
"""

def visualize(grid, seen):
    for r, row in enumerate(grid):
        line = ''
        for c, char in enumerate(row):
            line += 'O' if (r, c) in seen else char
        print(line)

@print_function
def part_one(input: str) -> int:
    grid = input.split('\n')
    s_pos = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 'S'][0]
    if is_example := (len(grid) < 20):
        total_steps = 6
    else:
        total_steps = 64
    print(f'{s_pos=}')
    stack = {s_pos}
    # print('\n' + '\n'.join(grid))
    for idx in range(total_steps):
        new_stack = set()
        while stack:
            r, c = stack.pop()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                out_of_bounds = not (0 <= rr < len(grid) and 0 <= cc < len(grid[0]))
                if out_of_bounds:
                    continue
                if grid[rr][cc] != '#':
                    new_stack.add((rr, cc))
        stack = new_stack
        # print(f'\nafter {idx+1} steps:')
        # visualize(grid, stack)
    # print(f'{len(seen)}=')
    # print(f'{len(stack)}= after {idx+1} steps')
    return len(stack)


    








@print_function
def part_two(input: str) -> int:
    lines = input.split('\n')
# @print_function
# def main(input: str) -> tuple[int, int]:
#     return (part_one(input), part_two(input))
if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print(part_one(input) == AOC_ANSWER[0])
    print(part_two(input) == AOC_ANSWER[1])
    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


