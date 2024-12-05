"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2507, 1969)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it

DIRS = [(x, y) for x, y in it.product([-1, 0, 1], repeat=2) if not (x == y == 0)]

@print_function
def part_one(input: str) -> int:
    """
    I feel like this could probably have been done a lot more elegant
    """
    grid = input.split('\n')
    # horizontal
    lines = grid.copy()
    # vertical
    for y in range(len(grid[0])):
        lines.append(''.join(grid[x][y] for x in range(len(grid))))
    # diagonals
    # u = x + y
    # v = x - y
    for u in range(len(grid)+len(grid[0])):
        chars = []
        for v in range(-len(grid[0]) + u % 2, len(grid), 2):
            x, y = (u + v) // 2, (u - v) // 2
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                chars.append(grid[x][y])
        lines.append(''.join(chars))
    for v in range(-len(grid[0]), len(grid)):
        chars = []
        for u in range(v % 2, len(grid)+len(grid[0]), 2):
            x, y = (u + v) // 2, (u - v) // 2
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                chars.append(grid[x][y])
        lines.append(''.join(chars))
    
    ans = sum(l.count('XMAS') + l.count('SAMX') for l in lines)
    return ans

import re
@print_function
def part_one(input: str, target: str = 'XMAS') -> int:
    """
    Marginally faster (~25%), but a lot more concise
    """
    grid = input.split('\n')
    width = len(grid[0])
    print(width, input.find('\n'))
    ans = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            # ## These three rows replace the next ~10 but are a factor 2 slower
            # for dx, dy in DIRS:
            #     if char == 'X' and 0 <= x+dx*3 < len(grid) and 0 <= y+dy*3 < len(grid[0]):
            #         ans += [grid[y+dy*step][x+dx*step] for step in range(len(target))] == list(target)
            if char != target[0]:
                continue
            for dx, dy in DIRS:
                if not (0 <= x+dx*3 < len(grid) and 0 <= y+dy*3 < len(grid[0])):
                    continue
                for step in range(1, len(target)):
                    if grid[y+dy*step][x+dx*step] != target[step]:
                        break
                else:
                    ans += 1
    return ans


@print_function
def part_two(input: str) -> int:
    grid = input.split('\n')
    ans = 0
    for y, row in enumerate(grid[1:-1], 1):
        for x, char in enumerate(row[1:-1], 1):
            if char == 'A' and \
                    {grid[y-1][x-1], grid[y+1][x+1]} == {'M', 'S'} and \
                    {grid[y-1][x+1], grid[y+1][x-1]} == {'M', 'S'}:
                ans += 1
    return ans



@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


