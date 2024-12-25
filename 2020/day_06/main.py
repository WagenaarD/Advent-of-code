"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (6911, 3473)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import Counter


@print_function
def part_one(input: str) -> int:
    score = 0
    for group in input.split('\n\n'):
        c = Counter(group.replace('\n', ''))
        score += len(c)
    return score

@print_function
def part_two(input: str) -> int:
    score = 0
    for group in input.split('\n\n'):
        persons = group.split('\n')
        for char in persons[0]:
            if all(char in person for person in persons):
                score += 1
    return score

@print_function
def main(input: str) -> tuple[int, int]:
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


