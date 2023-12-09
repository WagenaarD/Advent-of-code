"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 09:56
Part 1  - 09:12 - 12980
Part 2  - 09:23 - BRJLFULP
Cleanup - 
"""

import sys

x_current, x_list = 1, [1]
for line in sys.stdin.read().strip().split('\n'):
    if line != 'noop':
        x_list.append(x_current)
        x_current += int(line.split()[1])
    x_list.append(x_current)
print('Part 1:', sum([c * x_list[c - 1] for c in (20, 60, 100, 140, 180, 220)]))

output = ''.join(['#' if c % 40 + 1 in [x, x+1, x+2] else '.' for c,x in enumerate(x_list[:240])])
print('Part 2:\n' + '\n'.join([output[i:i+40] for i in range(0, 240, 40)]))