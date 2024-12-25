"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (175700056, 71668682)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re


def part_one(input: str) -> int:
    ans = 0
    for left, right in re.findall('mul\\((\\d+),(\\d+)\\)', input):
        ans += int(left) * int(right)
    return ans


def part_two(input: str) -> int:
    input = input.replace('\n', ' ')
    lines = re.findall('do\\(\\)(.*?)don\'t\\(\\)', f'do(){input}don\'t()')
    return sum(part_one(line) for line in lines)

    
@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


