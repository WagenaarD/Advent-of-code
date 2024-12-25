"""
From year folder:
../aoc_tools/aoc_start.sh xx && cd day_xx

Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = ('hxbxxyzz', 'hxcaabcc')

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

ALL_CHARS = 'abcdefghijklmnopqrstuvwxyz'
assert len(set(ALL_CHARS)) == 26
STRAIGHTS = [f'{c1}{c2}{c3}' for c1, c2, c3 in zip(ALL_CHARS, ALL_CHARS[1:], ALL_CHARS[2:])]
FORBIDDEN = 'iol'
DOUBLES = [char * 2 for char in ALL_CHARS]

def is_valid(password: str) -> bool:
    # Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    if not any(straight in password for straight in STRAIGHTS):
        return False
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    elif any(char in password for char in FORBIDDEN):
        return False
    # Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    elif sum(double in password for double in DOUBLES) < 2:
        return False
    else:
        return True
    

def increment(password: str) -> str:
    new_password = list(password)
    for idx in range(len(password) - 1, -1, -1):
        if new_password[idx] == 'z':
            new_password[idx] = 'a'
        else:
            new_password[idx] = chr(ord(new_password[idx]) + 1)
            break
    return ''.join(new_password)        


@print_function
def main(input: str) -> int:
    password = increment(input)
    ans = []
    for idx in range(2):
        while not is_valid(password):
            password = increment(password)
        ans.append(password)
        password = increment(password)
    return tuple(ans)

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


