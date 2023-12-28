"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 13:52:06
# 14:19:59
# 14:25:58

AOC_ANSWER = (7860, 8331)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run

DIRS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    '^': (-1,  0),
    'v': ( 1,  0),
}
REVERSED_DIRS = {v: k for k, v in DIRS.items()}


def solve(grid: list[str], beam: tuple[int, int, str]) -> int:
    new_beams = [beam]
    seen_states = set()
    while new_beams:
        beams = new_beams
        new_beams = []
        for r, c, dir in beams:
            dr, dc = DIRS[dir]
            rr, cc = r + dr, c + dc
            out_of_bounds = not (0 <= rr < len(grid) and 0 <= cc < len(grid[0]))
            if out_of_bounds:
                continue
            char = grid[rr][cc]
            if char == '.':
                new_beams.append((rr, cc, dir))
            elif char == '|':
                if dir in ('><'):
                    new_beams.append((rr, cc, '^'))
                    new_beams.append((rr, cc, 'v'))
                else:
                    new_beams.append((rr, cc, dir))
            elif char == '-':
                if dir in ('v^'):
                    new_beams.append((rr, cc, '<'))
                    new_beams.append((rr, cc, '>'))
                else:
                    new_beams.append((rr, cc, dir))
            elif char == '/':
                new_beams.append((rr, cc, REVERSED_DIRS[(-dc, -dr)]))
            elif char == '\\':
                new_beams.append((rr, cc, REVERSED_DIRS[(dc, dr)]))
            else:
                assert False, f'Unhandled char {char}'
        new_beams = [beam for beam in new_beams if not beam in seen_states]
        for beam in new_beams:
            seen_states.add(beam)
    seen_pos = set([(r, c) for r, c, _ in seen_states])
    return len(seen_pos)


@print_function
def part_one(grid: list[str]) -> int:
    beam = (0,-1,'>')
    return solve(grid, beam)


@print_function
def part_two(grid: list[str]) -> int:
    scores = []
    for r in range(len(grid)):
        scores.append(solve(grid, (r, -1, '>')))
        scores.append(solve(grid, (r, len(grid[0]), '<')))
    for c in range(len(grid[0])):
        scores.append(solve(grid, (-1, c, 'v')))
        scores.append(solve(grid, (len(grid), c, '^')))
    return max(scores)


def main(input: str) -> tuple[int, int]:
    grid = input.split('\n')
    return (part_one(grid), part_two(grid))
            

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')