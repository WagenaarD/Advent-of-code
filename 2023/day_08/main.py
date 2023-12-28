"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 09:23:08
# 09:31:06
# 11:16:57

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re
from functools import reduce
import math

AOC_ANSWER = (16579, 12927600769609)

def part_one(lines: list[str]) -> int:
    dirs = lines[0]
    words = [re.findall('\w+', line) for line in lines[2:]]
    elements = {word[0]: {'L': word[1], 'R': word[2]} for word in words}
    pos = 'AAA'
    for step_count, dir in enumerate(it.cycle(dirs)):
        if pos == 'ZZZ':
            break
        pos = elements[pos][dir]
    return step_count

def part_two(lines: list[str]) -> int:
    dirs = lines[0]
    words = [re.findall('\w+', line) for line in lines[2:]]
    elements = {word[0]: {'L': word[1], 'R': word[2]} for word in words}
    pos = [key for key in elements if key.endswith('A')]
    z_found = [False for _ in pos]
    for step_count, dir in enumerate(it.cycle(dirs), 1):
        pos = [elements[p][dir] for p in pos]
        for idx, p in enumerate(pos):
            if p[-1] == 'Z' and not z_found[idx]:
                z_found[idx] = step_count
        if all(z_found):
            break
    return reduce(math.lcm, z_found)

@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    return (part_one(lines), part_two(lines))


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')
