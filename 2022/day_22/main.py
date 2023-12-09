"""
Advent of code challenge 2022
>> python3 main.py < in
Part 1  - 67390
Part 2  - 95291

Assuming grid that goes like:
O--------> + x
|
|
|
V 
+ y
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache

DIR_SCORE = {
    (1, 0): 0,  # >
    (0, 1): 1,  # v
    (-1, 0): 2, # <
    (0, -1): 3, # ^
}

def rotate(dir: tuple, lr: str) -> tuple:
    return (-dir[1], dir[0]) if lr == 'R' else (dir[1], -dir[0])


def out_of_bounds(x: int, y: int, lines: list) -> bool:
    if 0 <= x < len(lines[0]) and 0 <= y < len(lines):
        return lines[y][x] == ' '
    return True

@print_function()
def find_last_position(lines: list, input: list, cube: bool = True, log: bool = False) -> int:
    console = lambda *x: print(*x) if log else lambda *x: None
    x, y, dir = lines[0].index('.'), 0, (1, 0)

    for command_idx, command in enumerate(input[:]):
        console('{}: (pos, dir, command) = {}'.format(command_idx, ((x, y), dir, command)))
        if command in ['R', 'L']:
            dir = rotate(dir, command)
            continue
        for idx in range(int(command)):
            # Move one step at a time
            dx, dy = dir
            next_dir = dir
            next_x, next_y = x + dx, y + dy
            if not cube:
                # Manage wrapping around (Part 1)
                while lines[(y + dy) % len(lines)][(x + dx) % len(lines[0])] == ' ':
                    dx += dir[0]
                    dy += dir[1]
                next_x, next_y = (x + dx) % len(lines[0]), (y + dy) % len(lines)
            else:
                # Manage wrapping around (Part 2)
                if out_of_bounds(next_x, next_y, lines):
                    # First find the current face
                    face_x = x % 50
                    face_y = y % 50
                    if x // 50 == 0 and y // 50 == 2:
                        # Black
                        if dx < 0:
                            next_x, next_y = 50, 49 - face_y
                            next_dir = (1, 0)
                        elif dy < 0:
                            next_x, next_y = 50, 50 + face_x
                            next_dir = (1, 0)
                    elif x // 50 == 0 and y // 50 == 3:
                        # Green
                        if dx < 0:
                            next_x, next_y = 50 + face_y, 0
                            next_dir = (0, 1)
                        elif dx > 0:
                            next_x, next_y = 50 + face_y, 149
                            next_dir = (0, -1)
                        elif dy > 0:
                            next_x, next_y = 100 + face_x, 0
                            next_dir = (0, 1)
                    elif x // 50 == 1 and y // 50 == 0:
                        # White
                        if dx < 0:
                            next_x, next_y = 0, 149 - face_y
                            next_dir = (1, 0)
                        elif dy < 0:
                            next_x, next_y = 0, 150 + face_x
                            next_dir = (1, 0)
                    elif x // 50 == 1 and y // 50 == 1:
                        # Blue
                        if dx < 0:
                            next_x, next_y = face_y, 100
                            next_dir = (0, 1)
                        elif dx > 0:
                            next_x, next_y = 100 + face_y, 49
                            next_dir = (0, -1)
                    elif x // 50 == 1 and y // 50 == 2:
                        # Yellow
                        if dx > 0:
                            next_x, next_y = 149, 49 - face_y
                            next_dir = (-1, 0)
                        elif dy > 0:
                            next_x, next_y = 49, 150 + face_x
                            next_dir = (-1, 0)
                    elif x // 50 == 2 and y // 50 == 0:
                        # Red
                        if dx > 0:
                            next_x, next_y = 99, 149 - face_y
                            next_dir = (-1, 0)
                        elif dy < 0:
                            next_x, next_y = face_x, 199
                            next_dir = (0, -1)
                        elif dy > 0:
                            next_x, next_y = 99, 50 + face_x
                            next_dir = (-1, 0)
                    console('  Changed cube face: {} -> {}'.format(
                        (x, y, dir), (next_x, next_y, next_dir))
                    )

            # Manage walls
            if lines[next_y][next_x] == '#':
                console('  Brick at {}'.format((next_x, next_y)))
                break
            elif lines[next_y][next_x] == '.':
                x, y, dir = next_x, next_y, next_dir
    console('(pos, dir, command) =', ((x, y), dir, 'DONE'))

    return 1000 * (y + 1) + 4 * (x + 1) + DIR_SCORE[dir]


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    lines = sys.stdin.read().split('\n')

    input = re.findall('[0-9]+|[LR]', lines[-1])
    lines.pop()
    lines.pop()
    width = max([len(line) for line in lines])
    lines = [line + ' ' * (width - len(line)) for line in lines]

    find_last_position(lines, input, False)
    find_last_position(lines, input, True)