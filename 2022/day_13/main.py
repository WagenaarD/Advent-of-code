"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - Forgot
Part 1  - Forgot - 6272
Part 2  - Forgot - 22288
Cleanup - 19:09
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import json
from functools import cmp_to_key


# @print_function(prefix = '   - ')
def correct_order(left, right) -> bool:
    """
    Copied from the challenge and reordered to fit the code.
    
    When comparing two values, the first value is called left and the second value is called right. 
    Then:
     - If exactly one value is an integer, convert the integer to a list which contains that integer
       as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2,
       convert the right value to [2] (a list containing 2); the result is then found by instead
       comparing [0,0,0] and [2].
     - If both values are lists, compare the first value of each list, then the second value, and so
       on. If the left list runs out of items first, the inputs are in the right order. If the right
       list runs out of items first, the inputs are not in the right order. If the lists are the
       same length and no comparison makes a decision about the order, continue checking the next
       part of the input.
     - If both values are integers, the lower integer should come first. If the left integer is 
       lower than the right integer, the inputs are in the right order. If the left integer is 
       higher than the right integer, the inputs are not in the right order. Otherwise, the inputs 
       are the same integer; continue checking the next part of the input.
    """
    if type(left) != type(right):
        left = left if type(left) == list else [left]
        right = right if type(right) == list else [right]
    if type(left) == type(right) == list:
        if type(left) == list:
            for idx in range(min(len(left), len(right))):
                result = correct_order(left[idx], right[idx])
                if result == 0:
                    continue
                else:
                    return result
            return min(1, max(-1, len(right) - len(left)))
        elif type(left) == int:
            return min(1, max(-1, right - left))            
    elif type(left) == type(right) == int:
        return min(1, max(-1, right - left))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    input = sys.stdin.read().strip()
    
    pairs = [[json.loads(line) for line in pair.split('\n')] for pair in input.split('\n\n')]
    print('Part 1:', sum([idx + 1 for idx, pair in enumerate(pairs) if correct_order(*pair) == 1]))

    lines = [json.loads(line) for line in input.replace('\n\n', '\n').split('\n')] + [[[2]], [[6]]]
    lines.sort(key = cmp_to_key(correct_order), reverse = True)
    print('Part 2:', (lines.index([[2]]) + 1) * (lines.index([[6]]) + 1))
