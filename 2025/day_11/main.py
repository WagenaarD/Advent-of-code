"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import cache

AOC_ANSWER = (599, 393474305030400)



class PathFinder:
    """
    A function made into a class so that the machine outputs can be stored once and not passed on 
    every function call. This is necessary to cache the function. You could also store the machine
    outputs outside the function scope, but I consider this bad practice as its messy and prone to 
    scope errors.
    """
    def __init__(self, machine_outputs: dict[str, list[str]]):
        self.machine_outputs = machine_outputs

    @cache
    def __call__(self, start: str, end: str):
        score = 0
        for dest in self.machine_outputs[start]:
            if dest == end:
                score +=1 
            else:
                score += self(dest, end)
        return score


@print_function
def part_one(input_txt: str) -> int:
    lines = input_txt.split('\n')
    mach_outputs = {line.split(': ')[0]: line.split(': ')[1].split() for line in lines}
    if 'you' not in mach_outputs: 
        return -1 # ex2
    path_finder = PathFinder(mach_outputs)
    return path_finder('you', 'out')


@print_function
def part_two(input_txt: str) -> int:
    lines = input_txt.split('\n')
    outputs = {line.split(': ')[0]: line.split(': ')[1].split() for line in lines}
    outputs['out'] = []
    if not all(a in outputs for a in ['svr', 'fft', 'dac']): 
        return -1 # ex1
    path_finder = PathFinder(outputs)
    return path_finder('svr', 'fft') * path_finder('fft', 'dac') * path_finder('dac', 'out') +\
            path_finder('svr', 'dac') * path_finder('dac', 'fft') * path_finder('fft', 'out')


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

# aoc_run( __name__, __file__, main, (5, -1), 'ex1')
# aoc_run( __name__, __file__, main, (-1, 2), 'ex2')
aoc_run( __name__, __file__, main, AOC_ANSWER)
