"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

AOC_ANSWER = (501, 1017)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

DIRS = [
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 0),
]


@print_function
def main(input_txt: str) -> tuple[int, int]:
    """
    Finds all paths from any 0 to any 9 and stores its start and end positions. Part 1 asks for the 
    number of unique 0-9 connections and part 2 the total number of connections.
    Since we only take paths with increasing height, we don't need to keep track of where we have 
    been. 
    """
    grid: dict[tuple[int, int], int] = {(r, c): int(char) for r, row in enumerate(input_txt.split('\n')) for c, char in enumerate(row)}
    nrows, ncols = input_txt.count('\n')+1, input_txt.find('\n')
    zeros: list[tuple[int, int]] = [pos for pos, char in grid.items() if char == 0]
    
    # connections is a list of all zero-nine connections. It contains tuples (zero_pos, nine_pos)
    connections: list[tuple[int, int]] = []
    for zero_pos in zeros:
        pos = zero_pos
        qeue = [pos]
        while qeue:
            pos = qeue.pop()
            # Look for directions in the 4 cardinal directions
            for dpos in DIRS:
                # npos is the next position (npos = pos + dpos for all axes)
                npos = tuple(x + dx for x, dx in zip(pos, dpos))
                # If out of bounds, skip this npos
                if not (npos[0] in range(nrows) and npos[1] in range(ncols)):
                    continue
                # We only consider paths with increasing height
                if grid[npos] != grid[pos] + 1:
                    continue
                # If we arrive at a peak, we store the result
                if grid[npos] == 9:
                    connections.append((zero_pos, npos))
                # If not a peak, we want to walk this path further
                else:
                    qeue.append(npos)
    return len(set(connections)), len(connections)

aoc_run(__name__, __file__, main, AOC_ANSWER)
