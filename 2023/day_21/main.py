"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (3642, 608603023105276)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import heapq


@print_function
def main(input, total_distance = 26501365):
    """
    Greatly improved algorithm. Determines distance to every coordinate in a 3x3 tile of grids
    centered around S. For the center tile, coordinates are scored normally. For adjacent tiles and
    corner tiles, the score is multiplied with how many similar tiles can be reached within the 
    total distance. This uses the fact that the outer and center rows and colums are unblocked.
    """
    grid = input.split('\n')
    s_pos = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 'S'][0]
    # True for my input, will be assumed throughout:
    assert len(grid) == len(grid[0])
    assert len(grid) % 2 == 1
    assert all(grid[r][s_pos[1]] in '.S' for r in range(len(grid)))
    assert all(grid[s_pos[0]][c] in '.S' for c in range(len(grid[0])))
    assert all(grid[r][0] == '.' for r in range(len(grid)))
    assert all(grid[r][-1] == '.' for r in range(len(grid)))
    assert all(grid[0][c] == '.' for c in range(len(grid[0])))
    assert all(grid[-1][c] == '.' for c in range(len(grid[0])))
    # Calculate distance in 3x3 grids surrounding center
    stack = [(0, *s_pos, 0, 0)]
    seen = {(*s_pos, 0, 0)}
    ans_p1 = 1
    ans_p2 = 0
    while stack:
        dist, r, c, gr, gc = heapq.heappop(stack) # heapq didnt really impact speed
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            grr = gr + (r + dr) // len(grid)
            gcc = gc + (c + dc) // len(grid[0])
            rr = (r + dr) % len(grid)
            cc = (c + dc) % len(grid[0])
            if (rr, cc, grr, gcc) in seen:
                continue
            if not (-1 <= grr <= 1 and -1 <= gcc <= 1):
                continue
            if grid[rr][cc] == '#':
                continue
            if (point_distance := dist + 1) > total_distance:
                continue
            if point_distance <= 64 and point_distance % 2 == 0:
                ans_p1 += 1
            seen.add((rr, cc, grr, gcc))
            heapq.heappush(stack, (point_distance, rr, cc, grr, gcc))
            # stack.append((point_distance, rr, cc, grr, gcc))
            # Grid distance: Number of grids in one dimension that contain this coordinate within 
            # the step limit
            grid_distance = 1 + (total_distance - point_distance) // len(grid)
            # Even weight = number of identical coordinates reached by taking an even number of 
            # steps within the step limit. Odd weight = same, but odd number of steps.
            if abs(grr) + abs(gcc) == 0:
                even_weight = 1
                odd_weight = 0
            elif abs(grr) + abs(gcc) == 1:
                # Adjacent grid: Total weight equal to grid distance.
                odd_weight = grid_distance // 2
                even_weight = grid_distance - odd_weight
            elif abs(grr) + abs(gcc) == 2:
                # Corner grid. Total weight is a triangle, so (distance**2 + distance) / 2. Starts
                # with 1 even, then 2 uneven, then +3 even, then +4 uneven etc.
                total_weight = (grid_distance**2 + grid_distance) // 2
                even_grid_distance = (grid_distance+1)//2
                even_weight = even_grid_distance**2
                odd_weight = total_weight - even_weight
            else:
                assert False
            if point_distance % 2 == total_distance % 2:
                ans_p2 += even_weight
            else:
                ans_p2 += odd_weight
    return ans_p1, ans_p2

 

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')
