"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (8997277, None)

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

def get_manual_idx(row, col):
    return (row**2 + col**2 + 2*row*col - 3*row - col + 2 ) // 2

def get_code_for_manual_idx(idx):
    code = 20151125
    for _ in range(idx-1):
        code = (code * 252533) % 33554393
    return code

def test_logic():
    from tabulate import tabulate
    idx_table = [[''] + [col for col in range(1, 7)]]
    code_table = [[''] + [col for col in range(1, 7)]]
    for row in range(1, 7):
        idx_table.append([row])
        code_table.append([row])
        for col in range(1, 7):
            manual_index = get_manual_idx(row, col)
            code = get_code_for_manual_idx(manual_index)
            idx_table[-1].append(manual_index)
            code_table[-1].append(code)
    print(tabulate(idx_table, tablefmt="simple_grid"))        
    print(tabulate(code_table, tablefmt="simple_grid"))

@print_function
def part_one(input_txt: str) -> int:
    row, col = map(int, re.findall('\\d+', input_txt))
    manual_idx = get_manual_idx(row, col)
    return get_code_for_manual_idx(manual_idx)
    






@print_function
def part_two(input_txt: str) -> int:
    row, col = re.findall('\\d+', input_txt)

    
    lines = input_txt.split('\n')
@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
