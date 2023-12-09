"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 11:39
Part 1  - 12:06 - 57838
Part 2  - 12:13 - 15077002392
Cleanup - 
"""

import sys
import re
import numpy as np
from pprint import pprint


def simulate_monkey_throws(monkeys, no_rounds = 20, divide = 3):
    test_product = np.prod([monkey['test'] for monkey in monkeys])
    for _ in range(no_rounds):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['inspected'] += 1
                item = eval(monkey['operation'].replace('old', 'item'))
                item %= test_product
                item //= divide
                target = monkey['targets'][item % monkey['test'] == 0]
                monkeys[target]['items'].append(item)
            monkey['items'] = []
    return monkeys


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    monkeys = [{
        'inspected': 0,
        'items': list(map(int, re.findall('[0-9]+', line_set[1]))),
        'operation': line_set[2][19:],
        'test': int(re.findall('[0-9]+', line_set[3])[0]),
        'targets': [int(re.findall('[0-9]+', line_set[row])[0]) for row in (4, 5)],
    } for line_set in [lines.split('\n') for lines in sys.stdin.read().strip().split('\n\n')]]

    monkeys_p1 = simulate_monkey_throws(monkeys, 20, 3)
    print('Part 1:', np.prod(sorted([monkey['inspected'] for monkey in monkeys_p1])[-2:]))

    monkeys_p2 = simulate_monkey_throws(monkeys, int(1E4), 1)
    print('Part 2:', np.prod(sorted([monkey['inspected'] for monkey in monkeys_p1])[-2:]))



