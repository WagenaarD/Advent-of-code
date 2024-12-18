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

AOC_ANSWER = (6568, 554865447501099)


@print_function
def part_one(input_txt: str) -> int:
    time, *bus_ids = map(int, re.findall('\\d+', input_txt))
    min_dt = float('inf')
    for bus_id in bus_ids:
        dt = bus_id - time % bus_id
        if dt < min_dt:
            min_dt = dt
            ans = dt * bus_id
    return ans


@print_function
def part_two(input_txt: str) -> int:
    """
    Needed to think for this. 
    """
    bus_ids = []
    for idx, bus_id in enumerate(input_txt.split('\n')[1].split(',')):
        if bus_id.isdigit():
            bus_ids.append((int(bus_id), (int(bus_id) - idx) % int(bus_id)))
    factor = 1
    offset = 0
    for bus_id, target_mod in bus_ids:
        for idx in range(bus_id):
            time = offset + factor * idx
            if time % bus_id == target_mod:
                factor *= bus_id
                offset = time
                break
    return offset


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


