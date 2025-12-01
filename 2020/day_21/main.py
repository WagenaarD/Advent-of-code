"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop, tuple_add, tuple_sub, tuple_mult, Pos
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache, reduce
from pprint import pprint

AOC_ANSWER = (2389, 'fsr,skrxt,lqbcg,mgbv,dvjrrkv,ndnlm,xcljh,zbhp')


@print_function
def main(input_txt: str) -> int:
    foods = []
    for line in input_txt.split('\n'):
        ingredients_txt, allergens_txt = line.split(' (contains ')
        foods.append((
            set(ingredients_txt.split(' ')), 
            set(allergens_txt[:-1].split(', ')),
        ))
    # Make sets of all encountered words
    elf_all = set(ing for food in foods for ing in food[0])
    eng_all = set(allerg for food in foods for allerg in food[1])
    # Determine which translations are (im)possible
    eng_to_elf_options = {eng: elf_all for eng in eng_all}
    for elfs, engs in foods:
        for eng in engs:
            eng_to_elf_options[eng] = eng_to_elf_options[eng] & elfs
    # Score p1
    possible_elf_allergens = set().union(*eng_to_elf_options.values())
    impossible_elf_allergens = elf_all - possible_elf_allergens
    score_p1 = 0
    for elfs, _ in foods:
        score_p1 += len(impossible_elf_allergens & elfs)
    # Find each allergen translation
    eng_to_elf_dict = {}
    while eng_to_elf_options:
        for eng in eng_to_elf_options:
            if len(eng_to_elf_options[eng]) > 1:
                continue
            elf = eng_to_elf_options[eng].pop()
            eng_to_elf_dict[eng] = elf
            eng_to_elf_options.pop(eng)
            for eng_other in eng_to_elf_options:
                if elf in eng_to_elf_options[eng_other]:
                    eng_to_elf_options[eng_other].remove(elf)
            break
    # answer for part to is a csv string. We print this as it is too long
    ans_p2 = ','.join([eng_to_elf_dict[allergen] for allergen in sorted(eng_to_elf_dict)])
    if __name__ == '__main__':
        # Executed if file is executed but not if file is imported. Necessary as the @print_function
        # shortens the answer.
        print(f'{ans_p2=}')

    return score_p1, ans_p2
        


aoc_run( __name__, __file__, main, AOC_ANSWER)
