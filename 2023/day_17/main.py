"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 13:46:18
# 13:47:11 PAUSE


AOC_ANSWER = (None, None)

import sys
sys.path.append('../..')
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
    '>': ( 0,  1),
    '<': ( 0, -1),
    'v': ( 1,  0),
    '^': (-1,  0),
}
INV_DIRS = {v:k for k,v in DIRS.items()}

    
@cache
def straight_path_score(pos: tuple[int, int], last_horizontal: bool) -> int:
    dir = (0,1) if last_horizontal else (1, 0)
    grid = straight_path_score.grid
    dims = len(grid), len(grid[0])
    to_go = tuple(d-p-1 for d, p in zip(dims, pos))
    if not any(to_go):
        return 0
    new_dir = [0, 0]
    for idx in range(2):
        if not dir[idx]:
            continue
        # last move was a row move, now only column moves allowed
        new_dir[idx] = 0
        if to_go[not idx] == 0:
            # If at the border, move one back
            new_dir[not idx], dist = -1, 1
        else:
            # Move towards the diagonal, move at least one and maximum three
            new_dir[not idx] = 1
            dist = min(3, max(1, to_go[not idx] - to_go[idx]))
    new_dir = tuple(new_dir)
    score = 0
    for d in range(1, dist + 1):
        score += grid[pos[0] + new_dir[0] * d][pos[1] + new_dir[1] * d]
    new_pos = tuple(p + nd * dist for p, nd in zip(pos, new_dir))
    return score + straight_path_score(new_pos, not last_horizontal)








@print_function()
def part_one(input: str) -> int:
    # grid = input.split('\n')
    grid = [[int(num) for num in line] for line in input.split('\n')]
    dims = len(grid), len(grid[0])
    straight_path_score.grid = grid
    # Fastest route, but a tricky rule
    #  - Cannot move >3 blocks in the same direction
    # A single step is a direction and a length 1-3        
    target = (len(grid) - 1, len(grid[0]) -1) 
    seen = {
        ((0,0),True): 0,
        ((0,0),False): 0,
    }
    # stack = {(pos, dir, sc) for (pos, dir), sc in seen.items()}
    stack = {((0,0),(0,1),0), ((0,0),(1,0),0)}
    score_threshold = 9 * (abs(target[0]) + abs(target[1]))

    while stack:
        pos, dir, score = stack.pop()
        # Pruning
        min_distance = sum(d - 1 - p for p, d in zip(pos, dims)) + score
        if min_distance >= score_threshold:
            continue
        # Adjust score threshold for pruning others
        max_distance = straight_path_score(pos, bool(dir[1])) + score
        if max_distance < score_threshold:
            print('New record:', pos, score, max_distance, len(stack))
            score_threshold = max_distance
        # Adjust dirs and add to stack
        for sign in (-1, 1):
            added_score = 0
            for dist in (1,2,3):
                new_dir = tuple(sign * d for d in reversed(dir))
                # new_dr = sign * dc
                # new_dc = sign * dr
                new_pos = tuple(p + dp * dist for p, dp in zip(pos, new_dir))
                # new_r = r + new_dr * dist
                # new_c = c + new_dc * dist
                # out_of_bounds = not (0 <= new_pos[0] < dims[0] and 0 <= new_pos[1] < dims[1])
                out_of_bounds = not all(0 <= p < d for p, d in zip(new_pos, dims))
                # print(dims, pos, tuple((0 <= p < d for p, d in zip(pos, dims))))
                # print(out_of_bounds)
                if out_of_bounds:
                    break
                added_score += grid[new_pos[0]][new_pos[1]]
                new_score = score + added_score
                # new_path = path + INV_DIRS[(new_dr, new_dc)] * dist
                tup = (new_pos, bool(new_dir[1]))
                if tup in seen:
                    if seen[tup] <= new_score:
                        continue
                seen[tup] = new_score
                stack.add((new_pos, new_dir, new_score))
    return score_threshold







    








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


