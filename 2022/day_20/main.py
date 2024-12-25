"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 9945 (ex 3)
Part 2  - 3338877775442 (ex )
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (9945, 3338877775442)
KEY = 811_589_153


def mix_list(input: list, key: int = 1, log: bool = False) -> list:
    output = input[:]
    key %= (len(output) - 1)
    for idx, num in sorted(input):
        pos = output.index((idx, num))
        new_pos = (pos + num * key) % (len(output) - 1)
        output.remove((idx, num))
        output.insert(new_pos, (idx, num))
    return output
    

def get_coord_sum(input: list) -> int:
    numbers_output = [num[1] for num in input]
    pos_0 = numbers_output.index(0)
    values = []
    for idx in [1000, 2000, 3000]:
        value = numbers_output[(pos_0 + idx) % len(numbers_output)]
        values.append(value)
    return sum(values)


@print_function()
def solve_1(input: list) -> int:
    output = mix_list(input)
    return get_coord_sum(output)


@print_function()
def solve_2(input: list, log: bool = False) -> int:
    for _ in range(10):
        input = mix_list(input[:], KEY)
    return get_coord_sum(input) * KEY


@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')
    input = list(enumerate(map(int, lines)))

    return (
        solve_1(input),
        solve_2(input),
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)
