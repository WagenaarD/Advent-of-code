"""
An exercise in Dijkstra algorithms as it is a common theme in AOC puzzles.

To use Dijkstra I had to make some changes
     - Always consider the item on the stack with the lowest distance (=score or cost) FIRST
     - Only takes steps of one
    Using these two changes, we can assume that whenever we arrive at a new position it will be the 
    quickest/cheapest path to that position 

heapq was very helpful in maintaining a sorted stack and saved a TON of time compared to using a 
list or set. It is relatively easy once you understand the use of heappop and heappush, but every-
thing is simple once you understand it.
"""
# Start, Part 1, Part 2
# 13:46:18
# 13:47:11 PAUSE
# 16:34:22


AOC_ANSWER = (1238, 1362)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
from functools import cache
from collections import deque
import heapq


def solve(input: str, step_bounds: tuple[int, int] = (1, 3)) -> int:
    """
    To use Dijkstra we should make some changes
     - Always consider the item on the stack with the lowest distance (=score or cost) FIRST
     - Only takes steps of one
    Using these two changes, we can assume that whenever we arrive at a new position it will be the 
    quickest/cheapest path to that position 
    """
    grid = [[int(num) for num in line] for line in input.split('\n')]
    # straight_path_score.grid = grid
    dims = len(grid), len(grid[0])
    target = dims[0] - 1, dims[1] - 1
    # Define starting conditions
    # seen: pos, direction, moved: cose
    stack = [
        (0,(0,0),(0,1),step_bounds[1]), # cost, pos, direction, moved
        (0,(0,0),(1,0),step_bounds[1]),
    ]
    seen = {((r,c),(dr,dc),dl): cost for cost,(r,c),(dr,dc),dl in stack}
    loop_idx = 0
    # Initiate loop
    while stack:
        if (loop_idx := loop_idx + 1) % 5000 == 0:
            print(f'{len(stack)=}')
        # Get the stack item with the lowest score
        cost, pos, dir, dl = heapq.heappop(stack)
        # Adjust dirs and add to stack
        for new_dir, new_dl in [((dir[1], dir[0]), 1), ((-dir[1], -dir[0]), 1), (dir, dl + 1)]:
            # Check if the move is valid
            new_pos = tuple(p + dp for p, dp in zip(pos, new_dir))
            within_bounds = all(0 <= p < d for p, d in zip(new_pos, dims))
            move_bound_valid = (new_dir == dir and new_dl <= step_bounds[1]) or (new_dir != dir and dl >= step_bounds[0])
            if not (within_bounds and move_bound_valid):
                continue
            # Check if reached state is new
            tup = (new_pos, new_dir, new_dl)
            if tup in seen:
                continue
            new_cost = cost + grid[new_pos[0]][new_pos[1]]
            seen[tup] = new_cost
            heapq.heappush(stack, (new_cost, new_pos, new_dir, new_dl))
    return min(cost for (pos, dir, dl), cost in seen.items() if pos == target)


@print_function
def main(input: str) -> tuple[int, int]:
    return (solve(input, (1, 3)), solve(input, (4, 10)))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    # print(solve(input, (1, 3)) == AOC_ANSWER[0])
    # print(solve(input, (4, 10)) == AOC_ANSWER[1])
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


