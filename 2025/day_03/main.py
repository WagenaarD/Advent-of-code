"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (17113, 169709990062889)


@print_function
def part_one(input_txt: str) -> int:
    """
    To get the highest joltage, we want the first character to be the highest possible which is the
    highest except if that is the rightmost value. We then look for the highest second character to
    the right of the left character.
    """
    lines = input_txt.split('\n')
    score_p1 = 0
    for line in lines:
        values = list(map(int, line))
        first_val = max(values[:-1])
        idx = values.index(first_val)
        second_val = max(values[idx+1:])
        joltage = int(str(first_val) + str(second_val))
        score_p1 += joltage
    return score_p1


@print_function
def solve(input_txt: str, length: int) -> int:
    """
    More general case of the solution shown in part_one. The output definition, appending and 
    joltage adding (indicated by ## below) can all be replaced by adding to joltage directly using:
        joltage += next_val * (10**idx)
    However, this may be less clear and is not really faster
    """
    lines = input_txt.split('\n')
    joltage = 0
    for line in lines:
        values = list(map(int, line))
        output = [] ##
        for idx in reversed(range(length)):
            if idx == 0:
                next_val = max(values)
            else:
                next_val = max(values[:-idx])
            val_pos = values.index(next_val)
            values = values[val_pos+1:]
            # joltage += next_val * (10**idx)
            output.append(next_val) ##
        joltage += int(''.join(str(char) for char in output)) ##
    return joltage

    
@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 2), 
        solve(input_txt, 12)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
