"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import numpy as np

AOC_ANSWER = (2743844, 6677951)


@print_function
def part_one(input_txt: str) -> int:
    df = np.array([list(map(int, line)) for line in input_txt.split('\n')])
    gamma_rate, epsilon_rate = 0, 0
    for col in range(df.shape[1]):
        gamma_rate <<= 1
        epsilon_rate <<= 1
        common_bit = bool(sum(df[:, col]) > (df.shape[0] / 2))
        gamma_rate += common_bit
        epsilon_rate += not common_bit
    return gamma_rate * epsilon_rate


@print_function
def part_two(input_txt: str) -> int:
    # Parse input
    df = np.array([list(map(int, line)) for line in input_txt.split('\n')])
    # Find oxygen rating. It is a single row of the input. Travel through columns, updating the 
    # filter as you go to only include rows that contain the most common (1 if equal) value. When 
    # the filter points to only one row, that is the bit representation of the oxygen rating.
    mask = np.ones(shape = (df.shape[0],)) == 1
    for col in range(df.shape[1]):
        common_bit = int(sum(df[mask, col]) >= (sum(mask) / 2))
        mask = (mask * (df[:, col] == common_bit)) == 1
        if sum(mask) == 1:
            oxygen_bits = df[mask,:][0]
            break
    oxygen = int(sum(val << idx for idx, val in enumerate(reversed(oxygen_bits))))
    # Determine co2 rating similarly, but now use the least common value (0 if equal).
    mask = np.ones(shape = (df.shape[0],)) == 1
    for col in range(df.shape[1]):
        uncommon_bit = int(sum(df[mask, col]) < (sum(mask) / 2))
        mask = (mask * (df[:, col] == uncommon_bit)) == 1
        if sum(mask) == 1:
            co2_bits = df[mask,:][0]
            break
    # Score is the product of both
    co2 = int(sum(val << idx for idx, val in enumerate(reversed(co2_bits))))
    return oxygen * co2

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
