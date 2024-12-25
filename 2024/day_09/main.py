"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (6_337_921_897_505, 6_362_722_604_045)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache, reduce
import math
from pprint import pprint


BLANK = '.'

def get_check_sum_old(disk_map: str):
    """Later solutions don't need this function (see below)"""
    return sum(idx * char for idx, char in enumerate(disk_map) if char != BLANK)

@print_function
def part_one_old(input: list[str]) -> int:
    """
    Found a better solution later (see below). 
    """
    ## Parse the input
    if len(input) % 2 == 1:
        input += '0'
    disk_map: list[str] = []
    for id, (nchar, nblank) in enumerate(zip(input[::2], input[1::2])):
        disk_map.extend([id] * int(nchar))
        disk_map.extend([BLANK] * int(nblank))
    if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]))

    # Defragment
    while BLANK in disk_map:
        idx = disk_map.index(BLANK)
        disk_map[idx] = disk_map.pop()
        while disk_map[-1] == BLANK:
            disk_map.pop()

    if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]))
    return get_check_sum_old(disk_map)

@print_function
def part_two_old(input_txt) -> int:
    """
    Found a better solution later (see below)
    """
    ## Parse the input
    if len(input_txt) % 2 == 1:
        input_txt += '0'
    disk_map: list[str] = []
    for id, (nchar, nblank) in enumerate(zip(input_txt[::2], input_txt[1::2])):
        disk_map.extend([id] * int(nchar))
        disk_map.extend([BLANK] * int(nblank))
    if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]))

    # Defragment
    char_idx = len(disk_map) - 1
    while char_idx > 0:
        if disk_map[char_idx] == BLANK:
            char_idx -= 1
            continue
        char = disk_map[char_idx]
        char_len = disk_map.count(char)
        char_idx -= char_len - 1 # move to beginning of char
        if char_idx-char_len < 0:
            # We dont want to move the first characted (even though it doesnt add to the checksum)
            char_idx -= 1
            continue 
        for blank_idx, blank_char in enumerate(disk_map[:char_idx]):
            if blank_char != BLANK:
                continue
            if all(c == BLANK for c in disk_map[blank_idx:blank_idx+char_len]):
                for idx in range(blank_idx, blank_idx + char_len):
                    disk_map[idx] = char
                for idx in range(char_idx, char_idx + char_len):
                    disk_map[idx] = BLANK
                if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]), f'moved {char}')
                break
        char_idx -= 1
    if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]))
    return get_check_sum_old(disk_map)


@print_function
def part_one(input_txt: list[str]) -> int:
    """
    We parse the input as a list of characters integers or '.'. The defragmentation is done looking 
    from left to right. If a number is found it is added to the checksum. If a blank is found, we 
    take the rightmost number and score it.
    ~100x faster than the old method
    """
    ## Parse the input
    disk_map: list[int] = []
    for id, char_len in enumerate(input_txt):
        disk_map.extend([id // 2 if id % 2 == 0 else BLANK] * int(char_len))
    if len(disk_map) < 100: print(''.join([str(el) for el in disk_map]))

    ## Defragment and scoring
    check_sum = 0
    for idx in range(len(disk_map)):
        if idx >= len(disk_map):
            break
        if disk_map[idx] != BLANK:
            check_sum += idx * disk_map[idx]
        else:
            check_sum += idx * disk_map.pop()
            while disk_map[-1] == BLANK:
                disk_map.pop()
    return check_sum


@print_function
def part_two(input_txt: str) -> int:
    """
    We store the input as a list of chars and spaces containing of each elements position and length.
    During the defragmentation, we traverse the list of characters reversely and look for a blank 
    space where it can be placed (to the left of its current position). If found, the spaces list is 
    updated. Since each element is only moved once, we can immediately add the checksum score to the
    answer and proceed to the next character.
    ~100x faster than the old method
    """
    ## Parse the input
    chars = []
    spaces = []
    pos = 0
    for id, char in enumerate(input_txt):
        if id % 2 == 0:
            chars.append((pos, int(char)))
        else:
            spaces.append((pos, int(char)))
        pos += int(char)
    
    ## Defragmentation and scoring
    check_sum = 0
    for char_id, (char_pos, char_len) in reversed(list(enumerate(chars))):
        for space_idx, (space_pos, space_len) in enumerate(spaces):
            if space_pos > char_pos:
                break
            if space_len >= char_len:
                spaces[space_idx] = (space_pos + char_len, space_len - char_len)
                char_pos = space_pos
                break
        check_sum += char_id * sum(range(char_pos, char_pos + char_len))
    
    return check_sum


@print_function
def main(input: str) -> tuple[int, int]:

    
    ## Run for both parts
    return (
        part_one(input), 
        part_two(input)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
