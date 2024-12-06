"""
From year folder:
../aoc_tools/aoc_start.sh xx && cd day_xx

Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (2640, 1102)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from dataclasses import dataclass
import re

@dataclass
class Deer:
    name: str
    speed: int
    run_time: int
    rest_time: int
    is_moving: bool = False
    time_left: int = 0
    distance: int = 0
    score: int = 0


@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    deers = []
    for line in lines:
        speed, run_time, rest_time = map(int, re.findall('\\d+', line))
        name = line.split()[0]
        deers.append(Deer(name, speed, run_time, rest_time))
    time_limit = 2503 if len(deers) > 2 else 1000
    for _ in range(time_limit):
        for deer in deers:
            deer: Deer
            if deer.time_left == 0:
                deer.is_moving = not deer.is_moving
                deer.time_left = deer.run_time if deer.is_moving else deer.rest_time
            if deer.is_moving:
                deer.distance += deer.speed
            deer.time_left -= 1
        max_distance = max(deer.distance for deer in deers)
        for deer in deers:
            if deer.distance == max_distance:
                deer.score += 1
    return max(deer.distance for deer in deers), max(deer.score for deer in deers)

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


