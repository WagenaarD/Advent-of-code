"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 
Part 2  - 3712643961892
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import cache
import operator


AOC_ANSWER = (170237589447588, 3712643961892)
OPERATIONS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


@cache
def monkey_val(name: str, humn_val: float = None) -> float:
    if name == 'humn' and humn_val != None:
        return humn_val
    elif name == 'root' and humn_val != None:
        command = monkey_val.input['root'][:5] + '-' + monkey_val.input['root'][6:]
    else:
        command = monkey_val.input[name]
    try:
        return float(command)
    except:
        operator = OPERATIONS[command[5]]
        left_val = monkey_val(command[0:4], humn_val)
        right_val = monkey_val(command[7:11], humn_val)
        return operator(left_val, right_val)
monkey_val.input = dict()


@print_function()
def solve_1():
    return int(monkey_val('root'))


@print_function()
def solve_2(max_iter: int = 25):
    """
    Newton algorithm.
     - f(x) is root_for_humn where x is humn_val.
     - Find f(x) = 0
     - determine df(x)/dx and f(x)
     - Shift x to the point where a linear extrapolation would hit f(x) = 0
    """
    dhumn_val = 100 if len(monkey_val.input) == 15 else 1000
    humn_val = monkey_val('humn')
    for _ in range(max_iter):
        root_val = monkey_val('root', humn_val)
        droot_dhumn = (monkey_val('root', humn_val + dhumn_val) - root_val) / dhumn_val
        humn_increment = round(-root_val / droot_dhumn)
        print('Iteration {}:\n - root_val = {}\n - humn_val = {}\n - droot/dhumn = {}\n - humn_val_increment = {}\n'.format(
            _, root_val, humn_val, droot_dhumn, humn_increment
        ))
        if root_val == 0:
            break
        humn_val += humn_increment
        if round(-root_val / droot_dhumn) < dhumn_val and dhumn_val > 10:
            dhumn_val //= 10

    return int(humn_val)


@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')
    monkey_val.input = {line[0:4]: line[6:] for line in lines}
    
    return (
        solve_1(),
        solve_2(),
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)
