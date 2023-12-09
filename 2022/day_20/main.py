"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 9945 (ex 3)
Part 2  - 3338877775442 (ex )
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function

KEY = 811_589_153


def mix_list(input: list, key: int = 1, log: bool = False) -> list:
    output = input[:]
    key %= (len(output) - 1)
    for idx, num in sorted(input):
        pos = output.index((idx, num))
        new_pos = (pos + num * key) % (len(output) - 1)
        output.remove((idx, num))
        output.insert(new_pos, (idx, num))
    return output
    

def get_coord_sum(input: list) -> int:
    numbers_output = [num[1] for num in input]
    pos_0 = numbers_output.index(0)
    values = []
    for idx in [1000, 2000, 3000]:
        value = numbers_output[(pos_0 + idx) % len(numbers_output)]
        values.append(value)
    return sum(values)


@print_function()
def solve_1(input: list) -> int:
    output = mix_list(input)
    return get_coord_sum(output)


@print_function()
def solve_2(input: list, log: bool = False) -> int:
    for _ in range(10):
        input = mix_list(input[:], KEY)
    return get_coord_sum(input) * KEY


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""

    lines = sys.stdin.read().strip().split('\n')
    input = list(enumerate(map(int, lines)))

    solve_1(input)
    solve_2(input)
