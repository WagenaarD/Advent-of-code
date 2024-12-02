"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (255, 55)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re

ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'

def is_nice_part_1(line):
    # A nice string is one with all of the following properties:
    #  - It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    if len(re.findall('[aeiou]', line)) < 3:
        return False
    #  - It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    for substr in ['ab', 'cd', 'pq', 'xy']:
        if substr in line:
            return False
    #  - It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    for char in ALPHABET_LOWER:
        if char * 2 in line:
            break
    else:
        return False
    return True
    
def is_nice_part_2(line):
    # Now, a nice string is one with all of the following properties:
    #  - It contains a pair of any two letters that appears at least twice in the string without 
    # overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    for c1, c2 in it.product(ALPHABET_LOWER, repeat=2):
        if line.count(c1 + c2) >= 2:
            break
    else:
        return False
    #  - It contains at least one letter which repeats with exactly one letter between them, like 
    # xyx, abcdefeghi (efe), or even aaa.
    for char in ALPHABET_LOWER:
        if re.search(char + '.' + char, line):
            break
    else:
        return False
    return True

@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    return (
        sum(is_nice_part_1(line) for line in lines), 
        sum(is_nice_part_2(line) for line in lines)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


