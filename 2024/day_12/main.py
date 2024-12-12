"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2
# st 2024-12-12 09-05-03 
# p1 2024-12-12 09-30-05 
# p2 2024-12-12 11-10-46 

AOC_ANSWER = (1494342, 893676)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def find_plants(r: int, c: int, grid: list[str], nrows: int, ncols: int) -> set[tuple[int, int]]:
    target_value = grid[r][c]
    qeue = [(r, c)]
    seen = {(r, c)}
    while qeue:
        r, c = qeue.pop()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if nr in range(nrows) and nc in range(ncols):
                if (nr, nc) not in seen:
                    if grid[nr][nc] == target_value:
                        seen.add((nr, nc))
                        qeue.append((nr, nc))
    return seen


def get_fences(plants, grid, nrows, ncols):
    """
    Old
    """
    fences = 0
    for r, c in plants:
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not (nr in range(nrows) and nc in range(ncols) and grid[nr][nc] == grid[r][c]):
                fences += 1
    return fences

def get_sides(plants: list[tuple[int, int]]) -> int:
    """
    Old
    Determines the number of sides. Calls get_1D_sides twice (horizontally and vertically).
    """
    return get_1D_sides(plants, True) + get_1D_sides(plants, False)

def get_1D_sides(plants: list[tuple[int, int]], horizontal: bool = True) -> int:
    """
    Old
    Checks for sides between rows. Seperately checks whether there are fences slightly above 
    (above_fence) or slighlty below (below_fence) the current line. When r = n, the line between 
    cells of row n and n-1 are checked. Therefore we need to iterate between 0 and n_rows + 1 
    (including). 
    Only counts a fence as a new side if the previously checked cell did not have the same fence.
    The script can be called for horizontal=false, which will flip the rows and columns so that it 
    detects vertical sides.
    """
    if horizontal:
        flip = lambda x: x
    else:
        flip = lambda x: (x[1], x[0])
    rows = set(flip(pos)[0] for pos in plants)
    cols = set(flip(pos)[1] for pos in plants)
    sides = 0
    for r in range(min(rows), max(rows)+2):
        below_fence, above_fence = False, False
        for c in range(min(cols), max(cols)+1):
            point = flip((r, c))
            up_point = flip((r-1, c))
            if (up_point in plants) and not point in plants:
                if not above_fence:
                    sides += 1
                above_fence = True
            else:
                above_fence = False
            if (point in plants) and not up_point in plants:
                if not below_fence:
                    sides += 1
                below_fence = True
            else:
                below_fence = False
    return sides



def get_fences_and_corners(plants: list[tuple[int, int]]) -> int:
    """
    Calculates the number of corners for a set of plants. An 
    .....
    .AAA.
    ..AA.
    .AAA.
    .....
    Consider the above structure. When iterating over all positions of A, we look for outer corners
    (where there is a gap on two adjacent cardinal directions) or inner corners (where there is no 
    gap ib twi adhacebt cardinal directions but there is a gap diagonally. Another way to define
    outer and inner corners is by imaging the fence traveling from the top left A along the top to 
    the right. The fence will turn right at an outer corner and left at an inner corner.
    """
    fences, corners = 0, 0
    for r, c in plants:
        for ((dr1, dc1), (dr2, dc2)) in zip(DIRS, DIRS[1:] + DIRS[:1]):
            adjacent_1 = r + dr1, c + dc1
            adjacent_2 = r + dr2, c + dc2
            diagonal = r + dr1 + dr2, c + dc1 + dc2
            if not adjacent_1 in plants:
                fences += 1
            if (not adjacent_1 in plants) and (not adjacent_2 in plants):
                corners += 1 # outer corner
            if adjacent_1 in plants and adjacent_2 in plants and not diagonal in plants:
                corners += 1 # inner corner
    return fences, corners
        


@print_function
def main(input_txt: str) -> tuple[int, int]:
    grid = input_txt.split('\n')
    nrows, ncols = len(grid), len(grid[0])
    seen = set()
    plots = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if (r, c) in seen:
                continue
            plants = find_plants(r, c, grid, nrows, ncols)
            seen.update(plants)
            area = len(plants)
            fences, sides = get_fences_and_corners(plants)
            # fences = get_fences(plants, grid, nrows, ncols)
            # sides = get_sides(plants)
            plots.append((val, area, fences, sides))
    p1, p2 = 0, 0
    for val, area, fences, sides in plots:
        p1 += area * fences
        p2 += area * sides
    return p1, p2
                    

aoc_run(__name__, __file__, main, AOC_ANSWER)


