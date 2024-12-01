"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (896, 659)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

@print_function
def main(input: str) -> 'tuple[int, int]':
    input = input.replace('B', '1').replace('R', '1').replace('F', '0').replace('L', '0')
    seat_ids = []
    for line in input.split('\n'):
        seat_ids.append(int(line, 2)) # I am very very smart
    seat_ids.sort()
    for seat_1, seat_2 in zip(seat_ids[8:-8], seat_ids[9:-8]):
        if seat_2 - seat_1 == 2:
            return max(seat_ids), seat_1 + 1


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


