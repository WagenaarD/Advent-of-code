"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - Forgot
Part 1  - Forgot - 391
Part 2  - Forgot - 386
Cleanup - Forgot
"""

import sys


def find_steps_between_points(start_positions: list, end_pos: tuple, lines: list) -> int:
    steps = 0
    visited = start_positions
    stack = start_positions[:]
    while not end_pos in visited and len(stack) > 0:
        for pos in stack[:]:
            for dir in ((1,0), (-1,0), (0,1), (0,-1)):
                new_pos = (pos[0] + dir[0], pos[1] + dir[1])
                if (0 <= new_pos[0] < len(lines) and 0 <= new_pos[1] < len(lines[0])) and \
                    (not new_pos in visited) and \
                    ord(lines[new_pos[0]][new_pos[1]]) - ord(lines[pos[0]][pos[1]]) <= 1:
                        visited.append(new_pos)
                        stack.append(new_pos)
            stack.remove(pos)
        steps += 1
    return steps

def find_positions(char: str, lines: list) -> list:
    return [(r, c) for r in range(len(lines)) for c in range(len(lines[0])) if lines[r][c] == char]

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""

    lines = sys.stdin.read().strip().split('\n')

    start_pos = find_positions('S', lines)[0]
    end_pos = find_positions('E', lines)[0]
    a_positions = find_positions('a', lines)
    lines = [line.replace('E', 'z').replace('S', 'a') for line in lines]

    print('Part 1:', find_steps_between_points([start_pos], end_pos, lines))
    print('Part 2:', find_steps_between_points(a_positions, end_pos, lines))