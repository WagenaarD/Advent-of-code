"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (1478097, None)


def loop_once(val, subject_number):
    return (val * subject_number) % 20201227


def get_loop_size(public_key: int):
    val = 1
    idx = 0
    while val != public_key:
        idx += 1
        val = loop_once(val, 7)
    return idx


def loop_n_times(subject_number, loop_number: int) -> int:
    val = 1
    for _ in range(loop_number):
        val = loop_once(val, subject_number)
    return val


@print_function
def main(input_txt: str) -> int:
    card_public_key, door_public_key = map(int, input_txt.split('\n'))
    card_loop_size = get_loop_size(card_public_key)
    # door_loop_size = get_loop_size(door_public)
    encryption_key = loop_n_times(door_public_key, card_loop_size)
    return (encryption_key, None)


aoc_run( __name__, __file__, main, AOC_ANSWER)
