"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (299, 1032)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict


def visualize(antennas, antinodes, nrows, ncols):
    grid = defaultdict(lambda : '.')
    for antinode in antinodes:
        grid[antinode] = '#'
    for key, positions in antennas.items():
        for pos in positions:
            grid[pos] = key
    print('\n'.join(''.join(grid[(r, c)] for c in range(ncols)) for r in range(nrows)))


@print_function
def main(input: str) -> tuple[int, int]:
    # Parse input
    grid = input.split('\n')
    antennas = defaultdict(list)
    nrows, ncols = len(grid), len(grid[0])
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != '.':
                antennas[val].append((r, c))
    
    # Determine antinodes
    antinodes_p1, antinodes_p2 = set(), set()
    for positions in antennas.values():
        for cur_pos, other_pos in it.permutations(positions, 2):
            for step in it.count():
                new_pos = tuple(x1 + step * (x1 - x2) for x1, x2 in zip(cur_pos, other_pos))
                if not (new_pos[0] in range(nrows) and new_pos[1] in range(ncols)):
                    break
                if step == 1:
                    antinodes_p1.add(new_pos)
                antinodes_p2.add(new_pos)
    
    # Print the grid for the example:
    if nrows == 12: 
        print(f'\nExample part 1:')
        visualize(antennas, antinodes_p1, nrows, ncols)
        print(f'\nExample part 2:')
        visualize(antennas, antinodes_p2, nrows, ncols)
    return len(antinodes_p1), len(antinodes_p2)

aoc_run(__name__, __file__, main, AOC_ANSWER)


