"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""

AOC_ANSWER = (2592, 2360)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

DIRS = {
    'v': ( 1, 0),
    '>': ( 0, 1),
    '^': (-1, 0),
    '<': ( 0,-1),
}

def get_visited(input: str) -> set:
    pos = (0, 0)
    visited = {pos}
    for char in input:
        dpos = DIRS[char]
        pos = tuple(map(sum, zip(pos, dpos)))
        visited.add(pos)
    return visited

@print_function
def part_one(input: str) -> int:
    return len(get_visited(input))

@print_function
def part_two(input: str) -> int:
    return len(get_visited(input[::2]) | get_visited(input[1::2]))
    
@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


