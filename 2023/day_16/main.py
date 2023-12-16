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
sys.path.append('../..')
from aoc_tools import print_function

DIRS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    '^': (-1,  0),
    'v': ( 1,  0),
}


def solve(grid, beam):
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
                if dir == '>':
                    new_beams.append((rr, cc, '^'))
                elif dir == '^':
                    new_beams.append((rr, cc, '>'))
                if dir == '<':
                    new_beams.append((rr, cc, 'v'))
                elif dir == 'v':
                    new_beams.append((rr, cc, '<'))
            elif char == '\\':
                if dir == '>':
                    new_beams.append((rr, cc, 'v'))
                elif dir == 'v':
                    new_beams.append((rr, cc, '>'))
                if dir == '<':
                    new_beams.append((rr, cc, '^'))
                elif dir == '^':
                    new_beams.append((rr, cc, '<'))
            else:
                assert False, 'Unhandled char'
        new_beams = [beam for beam in new_beams if not beam in seen_states]
        for beam in new_beams:
            seen_states.add(beam)
    
    seen_pos = set([(r, c) for r, c, _ in seen_states])

    return len(seen_pos)


@print_function()
def part_one(grid: 'list[str]') -> int:
    beam = (0,-1,'>')
    return solve(grid, beam)


@print_function()
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
            

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))