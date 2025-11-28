"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict

AOC_ANSWER = (395, 2296)


def energy_cycle_deposition(old_cells: set[tuple[int, int, int]], dim: int) -> set[tuple[int, int, int]]:
    """
    Uses deposition-point-of-view: Iterates through all possible new positions and calculates how 
    many neighbours that place has. 
    Intuitive and straightforward to program.
    """
    new_cells = set()
    min_x = min([min(pos[ax] for pos in old_cells) for ax in range(dim)])
    max_x = max([max(pos[ax] for pos in old_cells) for ax in range(dim)])
    for pos in it.product(range(min_x-1, max_x+2), repeat = dim):
        active_neighbours = 0
        for dpos in it.product([-1, 0, 1], repeat = dim):
            if all(dx == 0 for dx in dpos):
                continue
            npos = tuple(x + dx for x, dx in zip(pos, dpos))
            if npos in old_cells:
                active_neighbours += 1
                if active_neighbours == 4:
                    break
        if active_neighbours == 3 or (active_neighbours == 2 and pos in old_cells):
            new_cells.add(pos)
    return new_cells

def energy_cycle_interaction(old_cells: set[tuple[int, int, int]], dim: int) -> set[tuple[int, int, int]]:
    """
    Uses interaction-point-of-view. Iterates through all current positions and increment the 
    neigbours adjacent to that. After doing this for all positions, calculate which of these 
    positions meets the criteria to become active.
    Slightly less intuitive but ±100x faster.
    """
    new_cells = set()
    scores = defaultdict(int)
    for pos in old_cells:
        scores[pos] -= 1
        for dpos in it.product([-1, 0, 1], repeat = dim):
            npos = tuple(x + dx for x, dx in zip(pos, dpos))
            scores[npos] += 1
    for pos, active_neighbours in scores.items():
        was_active = pos in old_cells
        if active_neighbours == 3 or (active_neighbours ==2 and was_active):
            new_cells.add(pos)
    return new_cells


@print_function
def solve(input_txt: str, dimensions: int, iterations: int) -> int:
    cells = set()
    for row, line in enumerate(input_txt.split('\n')):
        for col, char in enumerate(line):
            if char == '#':
                cells.add((row, col) + (0,) * (dimensions - 2))
    for _ in range(iterations):
        cells = energy_cycle_interaction(cells, dimensions)
    return len(cells)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 3, 6), 
        solve(input_txt, 4, 6), 
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
