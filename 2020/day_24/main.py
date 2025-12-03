"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict

AOC_ANSWER = (263, 3649)
DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1), (0, 2), (0, -2))

def find_initial_coords(input_txt: str) -> list[tuple[int, int]]:
    """
    Find the coords on which the path ends. Only report positions on which an uneven amount of paths 
    end.
    
    :param input_txt: Basic AOC input
    :type input_txt: str
    :return: A list of black tile positions
    :rtype: list[tuple[int, int]]
    """
    lines = input_txt.split('\n')
    flipped = []
    for line in lines:
        pos = (0, 0)
        while line:
            if line.startswith('nw'):
                dpos = (-1, -1)
                line = line[2:]
            elif line.startswith('sw'):
                dpos = (1, -1)
                line = line[2:]
            elif line.startswith('ne'):
                dpos = (-1, 1)
                line = line[2:]
            elif line.startswith('se'):
                dpos = (1, 1)
                line = line[2:]
            elif line.startswith('w'):
                dpos = (0, -2)
                line = line[1:]
            elif line.startswith('e'):
                dpos = (0, 2)
                line = line[1:]
            else:
                raise(Exception('WTF'))
            pos = tuple(x + dx for x, dx in zip(pos, dpos))
        if pos in flipped:
            flipped.remove(pos)
        else:
            flipped.append(pos)
    return flipped


@print_function
def main(input_txt: str) -> tuple[int, int]:
    coords = find_initial_coords(input_txt)
    score_p1 = len(coords)
    # Process the dynamics
    for day in range(100):
        # First calculate all neighbours
        neighbours = defaultdict(int)
        for pos in coords:
            for dpos in DIRECTIONS:
                npos = tuple(x + dx for x, dx in zip(pos, dpos))
                neighbours[npos] += 1
        next_coords = []
        for pos in coords:
            # Any black tile with zero or more than 2 black tiles immediately adjacent to it is 
            # flipped to white.
            # Any black tile with 1 or 2 black neighbours stay black
            if neighbours[pos] in (1, 2):
                next_coords.append(pos)
        # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
        for pos in neighbours:
            if neighbours[pos] == 2 and pos not in coords:
                next_coords.append(pos)
        coords = next_coords
    score_p2 = len(coords)
    # Return the result
    return (
        score_p1, 
        score_p2,
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
