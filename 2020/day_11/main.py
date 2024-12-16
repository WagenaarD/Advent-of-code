"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import Tup

AOC_ANSWER = (2270, 2042)

DIRS = [Tup(elem) for elem in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]]

def process_round(grid: list[list[str]], nrows: int, ncols: int, p2: bool = False) -> list[list[str]]:
    """
    - If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes 
    occupied.
    - If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat 
    becomes empty.
    - Otherwise, the seat's state does not change.

    """
    ngrid = {}
    for r in range(nrows):
        for c in range(ncols):
            pos = Tup((r, c))
            val = grid[pos]
            if val != '.':
                if p2:
                    no_occupied = 0
                    for dpos in DIRS:
                        npos = pos + dpos
                        while npos in grid and grid[npos] == '.':
                            npos += dpos
                        if npos in grid and grid[npos] == '#':
                            no_occupied += 1
                else:
                    no_occupied = sum(grid[pos + dpos] == '#' for dpos in DIRS if pos+dpos in grid)
            if val == 'L' and no_occupied == 0:
                ngrid[pos] = '#'
            elif val == '#' and no_occupied >= (5 if p2 else 4):
                ngrid[pos] = 'L'
            else:
                ngrid[pos] = val
    return ngrid


@print_function
def solve(input_txt: str, p2: bool = False) -> int:
    grid = {Tup((r, c)): val for r, line in enumerate(input_txt.split('\n')) for c, val in enumerate(line)}
    nrows, ncols = input_txt.count('\n')+1, input_txt.find('\n')
    ngrid = process_round(grid, nrows, ncols, p2)
    while ngrid != grid:
        # print(1)
        grid, ngrid = ngrid, process_round(ngrid, nrows, ncols, p2)
    return sum(val == '#' for val in ngrid.values())


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt), 
        solve(input_txt, True)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


