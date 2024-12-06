"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""

AOC_ANSWER = (4559, 1604)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, print_loop


def simulate_guard_path(
        pos: tuple[int, int], 
        direction: tuple[int, int], 
        grid: list[str]
    ) -> tuple[bool, set[tuple[int, int]]]:
    visited = {pos}
    visited_dir = {(pos, direction)}
    loops = False
    while True:
        next_pos = tuple(x + dx for x, dx in zip(pos, direction))
        # Check out-of-bounds condition
        if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
            break
        # Turn right at obstacles (#)
        if grid[next_pos[0]][next_pos[1]] == '#':
            direction = (direction[1], -direction[0])
            continue
        # Move the guard and add new position to visited positions
        pos = next_pos
        visited.add(pos)
        # Check if the guard was here in this direction before
        if (pos, direction) in visited_dir:
            loops = True
            break
        visited_dir.add((pos, direction))
    return loops, visited

@print_function
def main(input: str) -> int:
    grid = input.split('\n')
    pos = [(x, row.find('^')) for x, row in enumerate(grid) if '^' in row][0]
    direction = (-1, 0) # up
    _, visited = simulate_guard_path(pos, direction, grid)
    p2 = 0
    for pos2 in print_loop(visited):
        # Copy the grid and place a obstacle (#) on the original guard path
        grid2 = grid.copy()
        grid2[pos2[0]] = grid2[pos2[0]][:pos2[1]] + '#' + grid2[pos2[0]][pos2[1]+1:] 
        loops, _ = simulate_guard_path(pos, direction, grid2)
        p2 += loops
    return len(visited), p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


