"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re
import itertools as it

AOC_ANSWER = (13105044880745, 3505392154485)


@print_function
def part_one(input_txt: str) -> int:
    reg = {}
    masks = [0, 0]
    for line in input_txt.split('\n'):
        if line.startswith('mask'):
            masks = [0, 0]
            for char in line.split(' = ')[1]:
                for idx in (0, 1):
                    masks[idx] = (masks[idx] << 1) + (char == str(idx))
        else:
            key, val = map(int, re.findall('\\d+', line))
            reg[key] = ~(~(val | masks[1]) | masks[0])
    return sum(reg.values())
             

@print_function
def part_two(input_txt: str) -> int:
    reg, mask_1s, mask_xs = {}, 0, []
    for line in input_txt.split('\n'):
        if line.startswith('mask'):
            mask_str = line.split(' = ')[1]
            mask_1s = int(mask_str.replace('X', '0'), 2)
            mask_xs = [2**(35-idx) for idx, char in enumerate(mask_str) if char == 'X']
        else:
            key, val = map(int, re.findall('\\d+', line))
            for values in it.product((True, False), repeat = len(mask_xs)):
                nkey = key | mask_1s
                for x_setting, idx in zip(values, mask_xs):
                    if x_setting: 
                        # force 1s
                        nkey = nkey | idx
                    else: 
                        # force 0s
                        nkey = ~(~nkey | idx)
                reg[nkey] = val
    return sum(reg.values())


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
