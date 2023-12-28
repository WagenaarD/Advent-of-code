"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 10:04:07
# 10:17:42 (leaderboard 04:10)
# 10:22:06 (leaderboard filled in 06:15)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import math

AOC_ANSWER = (1931, 83105)
BAG_CONFIG = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

@print_function
def main(input: str) -> tuple[int, int]:
    score_p1 = 0
    score_p2 = 0
    for idx, line in enumerate(input.split('\n')):
        _, sets_str = line.split(': ')
        legal_p1 = True
        min_p2 = {key: 0 for key in BAG_CONFIG}
        for cube_str in sets_str.replace(';', ',').split(', '):
            no_cubes_str, color = cube_str.split()
            min_p2[color] = max(min_p2[color], int(no_cubes_str))
            if int(no_cubes_str) > BAG_CONFIG[color]:
                legal_p1 = False
        if legal_p1:
            score_p1 += idx + 1
        score_p2 += math.prod(min_p2.values())
    return(score_p1, score_p2)
    
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')
    