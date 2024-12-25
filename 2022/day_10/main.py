"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 09:56
Part 1  - 09:12 - 12980
Part 2  - 09:23 - BRJLFULP
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (12980, 'BRJLFULP')

@print_function
def main(input_txt: str) -> tuple[int, int]:
    x_current, x_list = 1, [1]
    for line in input_txt.split('\n'):
        if line != 'noop':
            x_list.append(x_current)
            x_current += int(line.split()[1])
        x_list.append(x_current)
    output = ''.join(['#' if c % 40 + 1 in [x, x+1, x+2] else '.' for c,x in enumerate(x_list[:240])])
    print('\n'.join([output[i:i+40] for i in range(0, 240, 40)]))
    return (
        sum([c * x_list[c - 1] for c in (20, 60, 100, 140, 180, 220)]),
        'BRJLFULP', # This is what the output looks like in my image
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)