"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (None, None)


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    x_pos = 0
    depth = 0
    for line in lines:
        command, amount_txt = line.split(' ')
        amount = int(amount_txt)
        if command == 'up':
            depth -= amount
        elif command == 'down':
            depth += amount
        elif command == 'forward':
            x_pos += amount
        else:
            raise(Exception('WTF'))
    return x_pos * depth


@print_function
def part_two(input_txt: str) -> int:
    lines = input_txt.split('\n')
    x_pos = 0
    depth = 0
    aim = 0
    for line in lines:
        command, amount_txt = line.split(' ')
        amount = int(amount_txt)
        if command == 'up':
            aim -= amount
        elif command == 'down':
            aim += amount
        elif command == 'forward':
            x_pos += amount
            depth += amount * aim
        else:
            raise(Exception('WTF'))
    return x_pos * depth



@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
