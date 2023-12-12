"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# 06:35:18

AOC_ANSWER = (None, None)

import sys
sys.path.append('../..')
from aoc_tools import *
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict
import re
import numpy as np
from pprint import pprint
from functools import cache
import math

def blue_print_versions(bprint: str) -> 'list[str]':
    mtch = re.search('\?', bprint)
    idx = mtch.start()
    out = [bprint[:idx] + char + bprint[idx+1:] for char in '.#']
    if not '?' in out[0]:
        return out
    else:
        return blue_print_versions(out[0]) + blue_print_versions(out[1])

#     return [bprint[:idx] + char + bprint[idx+1:] for char in '.#']

# def get_all_combos(bprint: str) -> 'list[str]':
#     combos = replace_one(bprint)
#     for combo in combos:
#         if not '?' in combo:
#             continue
#         combos.remove(combo)
#         combos += replace_one(combo)
#     return combos


@print_function()
def main(input: str) -> int:
    lines = input.split('\n')
    ans = 0
    # .??..??...?##. 1,1,3
    for line_idx, line in enumerate(lines):
        print(line_idx, len(lines))
        # print('')
        # print(line)
        
        
        bprint, vals = line.split()
        score = [int(num) for num in vals.split(',')]
        # print(vals)
        for new_bprint in blue_print_versions(bprint):
            new_score = [len(mtch.group()) for mtch in re.finditer('\#+', new_bprint)]
            # print(new_bprint, new_score, score == new_score)
            if score == new_score:
                ans += 1



        # 
        # for iter_vals in it.permutations('#.', bprint.count('?')):
        # for iter_vals in it.combinations_with_replacement('#.', bprint.count('?')):
            
        #     new_line = bprint
        #     for mtch_idx, mtch in enumerate(re.finditer('\?', new_line)):
        #         char = iter_vals[mtch_idx]
        #         idx = mtch.start()
        #         new_line = new_line[:idx] + char + new_line[idx+1:]
        #         # print('', new_line)
        #     print(new_line, iter_vals)


            # for char in '.#':
            #     new_line = bprint[:idx-1] + char + bprint[idx:]
                
            #     cur_score = []
            #     while '?' in new_line:
            #         cur_mtch = re.search('\?+', new_line)
            #         cur_score.append(len(cur_mtch.group()))
            #         new_line = new_line[cur_mtch.start()+1:]
            #     if cur_score == score:
            #         ans += 1
        # break
    return ans













if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))


