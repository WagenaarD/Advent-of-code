"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (200_446, 238_317_474_993_392)

import sys
from pathlib import Path
from collections import defaultdict
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

MULTIPLICATION_FACTOR = 2024
PART_ONE_STEPS = 25
PART_TWO_STEPS = 75


def solve(input_txt: str, nsteps: int = PART_TWO_STEPS) -> int:
    """
    Simulates the transformations on stones according to the problem's rules:
    1. Stone with number 0 → replaced by stone engraved with 1.
    2. Stone with even number of digits → replaced by two stones:
       - Left and right halves of the digits engraved on separate stones.
    3. Stone with odd number of digits → replaced by one stone with the
       number multiplied by MULTIPLICATION_FACTOR.

    Args:
        input_txt (str): A string of space-separated integers representing stones.
        nsteps (int): Number of iterations of transformations.

    Returns:
        int: Total number of stones after all transformations.
    """
    stones_lst = tuple(map(int, input_txt.split()))
    stones = {key: stones_lst.count(key) for key in set(stones_lst)}

    for _ in range(nsteps):
        new_stones = defaultdict(int)
        for stone, count in stones.items():
            if stone == 0:
                new_stones[1] += count
            else:
                stone_str = str(stone)
                if len(stone_str) % 2 == 0:
                    # Split the digits and distribute the counts
                    left = int(stone_str[:len(stone_str) // 2])
                    right = int(stone_str[len(stone_str) // 2:])
                    new_stones[left] += count
                    new_stones[right] += count
                else:
                    # Multiply by the factor
                    new_stones[stone * MULTIPLICATION_FACTOR] += count
        stones = new_stones

    return sum(stones.values())


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, PART_ONE_STEPS), 
        solve(input_txt, PART_TWO_STEPS)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)

