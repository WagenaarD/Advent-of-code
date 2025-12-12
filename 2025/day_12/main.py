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
import math

AOC_ANSWER = (492, None)


@print_function
def part_one(input_txt: str) -> int:
    """
    Might be the ugliest solution I've ever written. Does not even work on example. but does work on
    input. I had no idea how to solve today as the numbers are quite large and any brute force 
    approach would take way too long. Instead, I tried to see how many regions were even possible
    simply by checking if they have enough open spaces (width * length) to acoomodate all the #'s. 
    It turns out this is already the right answer.
    """
    # Parse input
    *shapes_txt, regions_txt = input_txt.split('\n\n')
    shapes = {}
    shape_min_area = {}
    shape_max_area = {}
    for shape_txt in shapes_txt:
        name, *lines = shape_txt.split('\n')
        name_int = int(name[:1])
        shapes[name_int] = lines
        shape_min_area[name_int] = sum(line.count('#') for line in lines)
        shape_max_area[name_int] = sum(len(line) for line in lines)
        assert shape_max_area[name_int] == 9
    # If a the shapes fit without any overlapping, the shape definitely fits.
    # Also, if the shapes together have more '#' than there are open spaces in the area, the shapes
    # will defnitely not fit.
    # Combining these two provides a lower and upper bound. 
    score_p1_upper_bound = 0
    score_p1_lower_bound = 0
    for region_txt in regions_txt.split('\n'):
        start, end = region_txt.split(': ')
        total_area = math.prod(map(int, re.findall('\\d+', start)))
        min_shape_area = sum(cnt * shape_min_area[idx] for idx, cnt in enumerate(map(int, end.split())))
        max_shape_area = sum(cnt * shape_max_area[idx] for idx, cnt in enumerate(map(int, end.split())))
        score_p1_upper_bound += total_area >= min_shape_area
        score_p1_lower_bound += total_area >= max_shape_area
    # For my input these were the same, trivializing the problem
    print(f'{score_p1_lower_bound=}')
    print(f'{score_p1_upper_bound=}')
    if score_p1_lower_bound == score_p1_upper_bound:
        return score_p1_upper_bound
    else:
        return -1

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        None,
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
