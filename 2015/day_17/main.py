"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (1638, 17)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict


@print_function
def main(input: str) -> tuple[int, int]:
    containers = list(map(int, input.split('\n')))
    target = 25 if len(containers) == 5 else 150
    counter = defaultdict(int)
    for num_containers in range(1, len(containers)):
        for comb in it.combinations(containers, num_containers):
            if sum(comb) == target:
                counter[len(comb)] += 1
    return sum(counter.values()), counter[min(counter)]

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


