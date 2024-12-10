"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (501, None)

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
from functools import cache, reduce
import math
from pprint import pprint




DIRS = [
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 0),
]


@print_function
def part_one(input_txt: str) -> int:
    grid = input_txt.split('\n')
    grid = [[int(char) for char in row] for row in grid]
    nrows, ncols = len(grid), len(grid[0])
    zeros = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 0]
    score = 0
    for pos in zeros:
        seen = {pos}
        qeue = deque([pos])
        while qeue:
            pos = qeue.pop()
            for dpos in DIRS:
                npos = tuple(x + dx for x, dx in zip(pos, dpos))
                if not (npos[0] in range(nrows) and npos[1] in range(ncols)):
                    continue
                if npos in seen:
                    continue
                if grid[npos[0]][npos[1]] == grid[pos[0]][pos[1]] + 1:
                    seen.add(npos)
                    if grid[npos[0]][npos[1]] == 9:
                        score += 1
                    else:
                        qeue.append(npos)
    return score
                    




def dfs(pos, grid, nrows, ncols):
    score = 0
    for dpos in DIRS:
        npos = tuple(x + dx for x, dx in zip(pos, dpos))
        if not (npos[0] in range(nrows) and npos[1] in range(ncols)):
            continue
        if grid[npos[0]][npos[1]] == grid[pos[0]][pos[1]] + 1:
            if grid[npos[0]][npos[1]] == 9:
                score += 1
            else:
                score += dfs(npos, grid, nrows, ncols)
    return score




@print_function
def part_two(input_txt: str) -> int:
    grid = input_txt.split('\n')
    grid = [[int(char) for char in row] for row in grid]
    nrows, ncols = len(grid), len(grid[0])
    zeros = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 0]
    
    score = 0
    for pos in zeros:
        score += dfs(pos, grid, nrows, ncols)
    return score
    

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


