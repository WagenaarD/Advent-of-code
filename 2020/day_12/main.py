"""
Advent of code challenge
To run code, copy to terminal (MacOS):
pypy3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, Tup

AOC_ANSWER = (1645, 35292)
DIRS = {
    'N': Tup((-1, 0)),
    'E': Tup(( 0, 1)),
    'S': Tup(( 1, 0)),
    'W': Tup(( 0,-1)),   
}


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    pos = Tup((0, 0))
    dir = DIRS['E']
    for line in lines:
        cmd = line[0]
        val = int(line[1:])
        if cmd in DIRS:
            pos += DIRS[cmd] * val
        elif cmd == 'F':
            pos += dir * val
        elif cmd == 'L':
            for _ in range(val // 90):
                dir = dir.rotate_left()
        elif cmd == 'R':
            for _ in range(val // 90):
                dir = dir.rotate_right()
    return sum(abs(pos))


@print_function
def part_two(input_txt: str) -> int:
    lines = input_txt.split('\n')
    ship = Tup((0, 0))
    wayp = Tup((-1, 10))
    for line in lines:
        cmd = line[0]
        val = int(line[1:])
        if cmd in DIRS:
            wayp += DIRS[cmd] * val
        elif cmd == 'F':
            ship += wayp * val
        elif cmd == 'L':
            for _ in range(val // 90):
                wayp = wayp.rotate_left()
        elif cmd == 'R':
            for _ in range(val // 90):
                wayp = wayp.rotate_right()
    return sum(abs(ship))


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)
