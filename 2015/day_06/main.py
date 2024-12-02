"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (569999, 17836115)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

@print_function
def main(input: str) -> tuple[int, int]:
    grid_1 = [[False for _ in range(1000)] for _ in range(1000)]
    grid_2 = [[0 for _ in range(1000)] for _ in range(1000)]
    for line in input.split('\n'):
        command = re.match('[a-z ]+', line).group().strip()
        xs, ys, xe, ye = map(int, re.findall('\\d+', line))
        idx = 0
        for x in range(xs, xe+1):
            for y in range(ys, ye+1):
                idx += 1
                if command == 'turn on':
                    grid_1[x][y] = True
                    grid_2[x][y] += 1
                elif command == 'turn off':
                    grid_1[x][y] = False
                    grid_2[x][y] = max(grid_2[x][y] - 1, 0)
                elif command == 'toggle':
                    grid_1[x][y] = not grid_1[x][y]
                    grid_2[x][y] += 2
                else:
                    assert False
    p1 = sum([sum(line) for line in grid_1])
    p2 = sum([sum(line) for line in grid_2])
    return (p1, p2)

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


