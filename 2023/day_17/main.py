"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 13:46:18
# 13:47:11 PAUSE
# 16:34:22


AOC_ANSWER = (1238, 1362)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
from functools import cache

    
@cache
def straight_path_score(pos: tuple[int, int], last_horizontal: bool, step_bounds: tuple[int, int] = (1, 3)) -> int:
    """
    Calculates the distance using a "stupid" path straight to the bottom right end considering a min
    and max step length defined in step_bounds. The algorithm prefers to move and follow  the 
    diagonal originating from the target. 
    If the min step length > 1, the pathfinding can get "stuck" and would need to move backward. 
    Therefore, if the remainder is < 2*min step length, the algorithm moves to the edge in one go.
    """
    dir = (0,1) if last_horizontal else (1, 0)
    grid = straight_path_score.grid
    dims = len(grid), len(grid[0])
    to_go = tuple(d-p-1 for d, p in zip(dims, pos))
    if not any(to_go):
        return 0
    new_dir = [0, 0]
    for idx in range(2):
        if not dir[idx]:
            continue
        # last move was a row move, now only column moves allowed
        new_dir[idx] = 0
        if to_go[not idx] < step_bounds[0]:
            # If near the border, move back enough to be able to move 
            new_dir[not idx] = -1
            dist = step_bounds[0]
        elif to_go[not idx] < step_bounds[0] * 2:
            # Moving up to the diagonal would place us too close to finish. Move to the edge instead
            new_dir[not idx] = 1
            dist = to_go[not idx]
        else:
            # Move towards the diagonal, move at least one and maximum three
            new_dir[not idx] = 1
            dist = min(step_bounds[1], max(step_bounds[0], to_go[not idx] - to_go[idx]))
    new_dir = tuple(new_dir)
    score = 0
    for d in range(1, dist + 1):
        score += grid[pos[0] + new_dir[0] * d][pos[1] + new_dir[1] * d]
    new_pos = tuple(p + nd * dist for p, nd in zip(pos, new_dir))
    return score + straight_path_score(new_pos, not last_horizontal, step_bounds)


def solve(input: str, step_bounds: tuple[int, int] = (1, 3), log: bool = False) -> int:
    grid = [[int(num) for num in line] for line in input.split('\n')]
    straight_path_score.grid = grid
    dims = len(grid), len(grid[0])
    # Define starting conditions
    seen = {
        ((0,0),True): 0,
        ((0,0),False): 0,
    }
    stack = {((0,0),(0,1),0), ((0,0),(1,0),0)}
    score_threshold = 9 * (sum(dims) - 2)
    # Initiate loop
    while stack:
        pos, dir, score = stack.pop()
        # Pruning. If a shorter path is already found stop looking at this branch.
        min_distance = sum(d - 1 - p for p, d in zip(pos, dims)) + score
        if min_distance >= score_threshold:
            continue
        # Adjust score threshold for pruning other branches
        max_distance = straight_path_score(pos, bool(dir[1]), step_bounds) + score
        if max_distance < score_threshold:
            if log: print(f'New record! (pos: {pos}) (score: {score}) (max_d: {max_distance}) (stack: {len(stack)})')
            score_threshold = max_distance
        # Adjust dirs and add to stack
        for sign in (-1, 1):
            # New dirs are perpendicular to current dir
            new_dir = tuple(sign * d for d in reversed(dir))
            for dist in range(step_bounds[0], step_bounds[1] + 1):
                # Any distance between the min and max step length is considerd if they are not out
                # of bounds.
                new_pos = tuple(p + dp * dist for p, dp in zip(pos, new_dir))
                out_of_bounds = not all(0 <= p < d for p, d in zip(new_pos, dims))
                if out_of_bounds:
                    break
                added_score = sum(grid[pos[0] + new_dir[0] * d][pos[1] + new_dir[1] * d] for d in range(1, dist + 1))
                new_score = score + added_score
                # If the new position has already previously been reached more quickly, there is no
                # need to investigate this branch further.
                tup = (new_pos, bool(new_dir[1]))
                if tup in seen:
                    if seen[tup] <= new_score:
                        continue
                seen[tup] = new_score
                stack.add((new_pos, new_dir, new_score))
    return score_threshold


@print_function
def main(input: str, log: bool = False) -> tuple[int, int]:
    return (solve(input, (1, 3), log), solve(input, (4, 10), log))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input, True) == (AOC_ANSWER[0], AOC_ANSWER[1]))


