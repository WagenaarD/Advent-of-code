"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 12:22:53

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

DIRS = {
    'D': ( 1,  0),
    'U': (-1,  0),
    'R': ( 0,  1),
    'L': ( 0, -1),
}

def visualize_part_one(trench: set[tuple[int, int]], seen: set[tuple[int, int]] = set()) -> None:
    
    r_min = min(r for r, c in (trench | seen))
    r_max = max(r for r, c in (trench | seen))
    c_min = min(c for r, c in (trench | seen))
    c_max = max(c for r, c in (trench | seen))
    for r in range(r_min, r_max + 1):
        out = ''
        for c in range(c_min, c_max + 1):
            out += '#' if (r,c) in trench else '~' if (r, c) in seen else '.'
        print(out)


@print_function()
def part_one(input: str) -> int:
    lines = input.split('\n')
    trench = set()
    pos = (0,0)
    for line in lines:
        dr, dl, color = line.split()
        dr = DIRS[dr]
        for _ in range(int(dl)):
            pos = tuple(p + dp for p, dp in zip(pos, dr))
            trench.add(pos)
    # visualize_part_one(trench)
    
    # Grow from outside
    r_min = min(r for r, c in trench) - 1
    r_max = max(r for r, c in trench) + 1
    c_min = min(c for r, c in trench) - 1
    c_max = max(c for r, c in trench) + 1
    stack = set([(r, c_min) for r in range(r_min, r_max+1)] + \
        [(r, c_max) for r in range(r_min, r_max+1)] + \
        [(r_min, c) for c in range(c_min, c_max+1)] + \
        [(r_max, c) for c in range(c_min, c_max+1)])
    seen = stack.copy()
    while stack:
        r,c = stack.pop()
        for dr, dc in DIRS.values():
            new_pos = (r + dr, c + dc)
            in_bounds = r_min <= new_pos[0] <= r_max and c_min <= new_pos[1] <= c_max
            if in_bounds and new_pos not in seen and new_pos not in trench:
                seen.add(new_pos)
                stack.add(new_pos)
    # visualize_part_one(trench, seen)
    ans = 0
    for r in range(r_min, r_max + 1):
        for c in range(c_min, c_max + 1):
            if not (r,c) in seen:
                ans +=1 
    return ans


@print_function()
def part_two(input: str) -> int:
    lines = input.split('\n')





    
# @print_function()
# def main(input: str) -> tuple[int, int]:
#     return (part_one(input), part_two(input))
if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print(part_one(input) == AOC_ANSWER[0])
    print(part_two(input) == AOC_ANSWER[1])
    # print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


