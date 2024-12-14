"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""


AOC_ANSWER = (208437768, 7492)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re
import math


def visualize_bots(bots):
    """
    Prints the bots in a grid. Useful for testing example input or looking for visual patterns in 
    part 2.
    """
    width, height = (101, 103) if len(bots) > 100 else (11, 7)
    positions = [(r, c) for r, c, _, _ in bots]
    out = []
    for r in range(height):
        row = []
        for c in range(width):
            cnt = positions.count((r, c))
            row.append(str(cnt) if cnt else '.')
        out.append(''.join(row))
    print('\n'.join(out))


def move(bots: list[tuple[int, int, int, int]], step: int) -> None:
    """
    Moves the bots by a specified number of steps. If bots get out-of-bounds they loop around the 
    grid (grid is doughnut shaped).
    """
    width, height = (101, 103) if len(bots) > 100 else (11, 7)
    for idx, (r, c, dr, dc) in enumerate(bots):
        if step == 2: print(r, dr, height, (r + dr * step), (r + dr * step) % height)
        r = (r + dr * step) % height
        c = (c + dc * step) % width
        bots[idx] = (r, c, dr, dc)


def score_bots(bots: list[tuple[int, int, int, int]]) -> None:
    """
    Scores the number of bots in four quadrants and returns their product. Bots on the center line
    are ignored.
    Returns by argument
    Required for part one
    """
    width, height = (101, 103) if len(bots) > 100 else (11, 7)
    quadrants = [0, 0, 0, 0]
    for r, c, _, _ in bots:
        if r < (height // 2):
            if c < (width // 2):
                quadrants[0] += 1
            elif c > (width // 2):
                quadrants[1] += 1
        elif r > (height // 2):
            if c < (width // 2):
                quadrants[2] += 1
            elif c > (width // 2):
                quadrants[3] += 1
    return math.prod(quadrants)


@print_function
def part_one(input_txt: str) -> int:
    """
    Find the position of each bot after 100 steps, then score the bots according to quadrants
    """
    bots = []
    for line in input_txt.split('\n'):
        bots.append(list(map(int, re.findall('-?\\d+', line))))
    bots = [(r, c, dr, dc) for c, r, dc, dr in bots]
    move(bots, 100)
    return score_bots(bots)


def get_max_connected_components(bots: list[tuple[int, int, int, int]]) -> int:
    """
    Calculates the size of the number of bots in the largest connected component.
    """
    cc = []
    seen = set()
    positions ={(r, c) for r, c, _, _ in bots}
    for botr, botc in positions:
        if (botr, botc) in seen:
            continue
        cc.append(1)
        qeue = [(botr, botc)]
        while qeue:
            r, c = qeue.pop()
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in positions and (nr, nc) not in seen:
                    qeue.append((nr, nc))
                    cc[-1] += 1
                    seen.add((nr, nc))
    return max(cc)
    

@print_function
def part_two(input_txt: str, visualize: bool = False) -> int:
    """
    Find how many steps are required for the "christmas tree easter egg" to show. There is no 
    definition given on what this tree would look like. However I made two correct assumptions:
    - First attempt: When the christmas tree shows, all robots have unique positions. This worked 
    for my input, but I'm not sure if it will work for all inputs.
    - Second attempt: When the christmas tree shows, there are larger connected components of bots.
    Normally there are less than 25 connected bots, but when the tree shows there are over 200.
    """
    bots = []
    for line in input_txt.split('\n'):
        bots.append(list(map(int, re.findall('-?\\d+', line))))
    bots = [(r, c, dr, dc) for c, r, dc, dr in bots]
    if len(bots) < 100:
        return None
    ccs = []
    for idx in it.count(1):
        move(bots, 1)
        # positions = [(r, c) for r, c, _, _ in bots]
        # positions_unique = len(positions) == len(set(positions)) # first method
        # if len(positions) == len(set(positions)):
        ccs.append(get_max_connected_components(bots)) # second method
        if ccs[-1] > 100:
            print(f'current #of connected components {ccs[-1]}. Five highest = {list(sorted(ccs))[-5:]}')
            if visualize: 
                print(f'\nAfter {idx} seconds')
                visualize_bots(bots)
            return idx


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt),
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


