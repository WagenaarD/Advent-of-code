"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 11:39
Part 1  - 12:06 - 57838
Part 2  - 12:13 - 15077002392
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re
import numpy as np
import math
from pprint import pprint

AOC_ANSWER = (57838, 15050382231)


def simulate_monkey_throws(monkeys, no_rounds = 20, divide = 3, log = False):
    test_product = math.prod([monkey['test'] for monkey in monkeys])
    for _ in range(no_rounds):
        for idx, monkey in enumerate(monkeys):
            # if log: print(f'Monkey {idx}:')
            while monkey['items']:
                item = monkey['items'].pop(0)
                # if log: print(f'  Monkey inspects an item with a worry level of {item}.')
                monkey['inspected'] += 1
                item = eval(monkey['operation'].replace('old', 'item'))
                item %= test_product
                # if log: print(f'    Worry level changed to {item}.')
                item //= divide
                # if log: print(f'    Worry level divided by 3 to {item}.')
                divisible = item % monkey['test'] == 0
                # if log: print(f'    Current worry level is {""if divisible else "not "}divisible by {monkey["test"]}.')
                target = monkey['targets'][item % monkey['test'] == 0]
                # if log: print(f'    Item with worry level {item} is thrown to monkey {target}.')
                monkeys[target]['items'].append(item)
    return monkeys

def solve(input_txt: str, no_rounds: int, divide: int) -> int:
    monkeys = [{
        'inspected': 0,
        'items': list(map(int, re.findall('[0-9]+', line_set[1]))),
        'new_items': [],
        'operation': line_set[2][19:],
        'test': int(re.findall('[0-9]+', line_set[3])[0]),
        'targets': [int(re.findall('[0-9]+', line_set[row])[0]) for row in (4, 5)][::-1],
    } for line_set in [lines.split('\n') for lines in input_txt.split('\n\n')]]
    monkeys = simulate_monkey_throws(monkeys, no_rounds, divide)
    scores = list(sorted(monkey['inspected'] for monkey in monkeys))
    return math.prod(scores[-2:])


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, 20, 3),
        solve(input_txt, 10_000, 1)
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)
