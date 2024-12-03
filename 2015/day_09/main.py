"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (141, 736)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
from collections import defaultdict
import re


@print_function
def main(input: str) -> 'tuple[int, int]':
    lines = input.split('\n')
    dist = defaultdict(dict)
    for line in lines:
        place1, place2, d = re.match('(\w+) to (\w+) = (\d+)', line).groups()
        dist[place1][place2] = int(d)
        dist[place2][place1] = int(d)
    traveled = []
    for places in it.permutations(dist.keys(), len(dist)):
        current = places[0]
        traveled.append(0)
        for place in places[1:]:
            traveled[-1] += dist[current][place]
            current = place
    return min(traveled), max(traveled)


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


