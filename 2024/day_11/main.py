"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (200446, 238317474993392)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from collections import defaultdict

            
print_function
def solve(input_txt: str, nsteps: int = 75) -> int:
    """
    Processes the following rules:
    1. If the stone is engraved with the number 0, it is replaced by a stone engraved with the 
            number 1.
    2. If the stone is engraved with a number that has an even number of digits, it is 
            replaced by two stones. The left half of the digits are engraved on the new left 
            stone, and the right half of the digits are engraved on the new right stone. 
            (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    3. If none of the other rules apply, the stone is replaced by a new stone; the old 
            stone's number multiplied by 2024 is engraved on the new stone.
    
    For part one (25 iterations) I initially stored stones as a list of stones, but that was too 
    slow for part 2 (75 iterations). When trying the calculations manually I figured out that the 
    order of stones doesnt matter and certain values are repeated so that it might be more efficient
    to store a counter of all types of stones. This turned out to be very fast (<0.1s).
    """
    stones_lst = tuple(map(int, input_txt.split()))
    stones = {key: stones_lst.count(key) for key in set(stones_lst)}
    for _ in range(nsteps):
        nstones = defaultdict(int)
        for stone, stone_count in stones.items():
            if stone == 0:
                nstones[1] += stone_count
            elif len(stone_str := str(stone))%2==0:
                nstones[int(stone_str[:len(stone_str)//2])] += stone_count
                nstones[int(stone_str[len(stone_str)//2:])] += stone_count
            else:
                nstones[stone*2024] += stone_count
        stones = nstones
    return sum(nstones.values())

            






@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 25), 
        solve(input_txt, 75)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


# 0
# 1
# 2024
# 20 24
# 2 * 2 4
# 4048 * 4048 8096
# 40 48 * 40 48 80 96
# 4 * 4 8 * 4 * 4 8