"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (3642, 608603023105276)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function
import heapq


def visualize(grid, seen):
    for r, row in enumerate(grid):
        line = ''
        for c, char in enumerate(row):
            line += 'O' if (r, c) in seen else char
        print(line)


def part_one(input: str) -> int:
    grid = input.split('\n')
    s_pos = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 'S'][0]
    if is_example := (len(grid) < 20):
        total_steps = 6
    else:
        total_steps = 64
    stack = {s_pos}
    for idx in range(total_steps):
        new_stack = set()
        while stack:
            r, c = stack.pop()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = r + dr, c + dc
                out_of_bounds = not (0 <= rr < len(grid) and 0 <= cc < len(grid[0]))
                if out_of_bounds:
                    continue
                if grid[rr][cc] != '#':
                    new_stack.add((rr, cc))
        stack = new_stack
    return len(stack)


def advance_one(grid:list[str], in_grid: list[list[list[tuple[int,int]]]], stack: set[tuple[int,int]]):
    """
    Takes one more step and stores which grid locations are reached in which grid. Grids are 
    indicated by loop_r and loop_c.
    """
    new_stack = set()
    while stack:
        r, c, loop_r, loop_c  = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            loop_rr = loop_r + (r + dr) // len(grid)
            loop_cc = loop_c + (c + dc) // len(grid[0])
            rr = (r + dr) % len(grid)
            cc = (c + dc) % len(grid[0])
            if grid[rr][cc] == '#':
                continue
            if (loop_rr, loop_cc) in in_grid[rr][cc]:
                continue
            in_grid[rr][cc].append((loop_rr, loop_cc))
            new_stack.add((rr, cc, loop_rr, loop_cc))
    return new_stack


def get_score(in_grid: list[list[list[tuple[int, int]]]], total_steps: int) -> int:
    """
    Calculates all locations that have been reached and that are reached in an even or uneven number 
    of steps (depending on the total number of steps).
    """
    ans = 0
    for r, row in enumerate(in_grid):
        for c, in_gs in enumerate(row):
            for loop_r, loop_c in in_gs:
                ans += (r + c + loop_r + loop_c) % 2 == total_steps % 2
    return ans


def part_two(input: str, total_steps: int = 26501365) -> int:
    """
    Sped up significantly compared to part one. No longer keep track of all possible paths but track
    which locations are within reach. Afterwards, whether they are reacheable depends on whether it
    takes an even or uneven number of steps to reach that location.
    Next improvement is to look for a repeating pattern. The score is a quadratic function.
    """
    grid = input.split('\n')
    s_pos = [(r, c) for r, row in enumerate(grid) for c, char in enumerate(row) if char == 'S'][0]
    # True for my input, will be assumed throughout:
    assert len(grid) % 2 == 1
    assert len(grid[0]) % 2 == 1
    assert s_pos[0] == len(grid) // 2
    assert s_pos[1] == len(grid[0]) // 2
    assert all(grid[r][s_pos[1]] in '.S' for r in range(len(grid)))
    assert all(grid[s_pos[0]][c] in '.S' for c in range(len(grid[0])))
    # in_grid describes in which grids the value has been reached
    in_grid = [[[] for c in row] for r, row in enumerate(grid)]
    in_grid[s_pos[0]][s_pos[1]].append((0,0))
    stack = {(*s_pos, 0, 0)}
    # The edge of the grid will be reached after half a grid length. Afterwardsm, new grids are 
    # reached every (len(grid)) iterations. Scores are different every grid since the moves required 
    # to reach them are uneven. Therefore, scores follow a pattern every two grid lengths.
    loop_offset = s_pos[0]
    loop_length = len(grid) * 2
    assert (total_steps - loop_offset) % loop_length == 0, 'True for my input'
    fit_scores = []
    for idx in range(total_steps):
        if (idx-loop_offset) % loop_length == 0:
            fit_scores.append(get_score(in_grid, total_steps))
        if len(fit_scores) >= 3:
            break
        stack = advance_one(grid, in_grid, stack)
    diff_1_0 = fit_scores[1] - fit_scores[0]
    diff_2_1 = fit_scores[2] - fit_scores[1]
    a = (diff_2_1 - diff_1_0) // 2
    c = fit_scores[0]
    b = fit_scores[1] - a - c
    extrapolated_score = lambda x: x**2 * a + x * b + c
    total_loops = (total_steps - loop_offset) // loop_length
    return extrapolated_score(total_loops)

@print_function
def main(input: str) -> tuple[int, int]:
    return (part_one(input), part_two(input))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))
