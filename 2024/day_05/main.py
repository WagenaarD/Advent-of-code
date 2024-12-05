"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (6041, 4884)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it


class UpdateRules:
    def __init__(self, rules_txt: 'dict'):
        self.rules: 'dict[tuple[int, int], bool]' = {}
        for line in rules_txt.split('\n'):
            num1, num2 = map(int, line.split('|'))
            self.rules[(num1, num2)] = True
            self.rules[(num2, num1)] = False
    
    def is_valid(self, update: 'list[int]') -> bool:
        for nums in it.combinations(update, 2):
            if nums in self.rules:
                if not self.rules[nums]:
                    return False
        return True

    def sort(self, update: 'list[int]') -> 'list[int]':
        """
        Recursive sort. Looks for an error, then swaps the numbers and tries again. If no error is 
        found the original update is returned.
        """
        for nums in it.combinations(update, 2):
            if nums in self.rules:
                if not self.rules[nums]:
                    # swap em and start again
                    idxs = [update.index(num) for num in nums]
                    update[idxs[0]] = nums[1]
                    update[idxs[1]] = nums[0]
                    return self.sort(update)
        # no erorrs found, return current solution
        return update


@print_function
def main(input: str) -> tuple[int, int]:
    rules_txt, updates_txt = input.split('\n\n')
    update_rules = UpdateRules(rules_txt)
    updates = [list(map(int, line.split(','))) for line in updates_txt.split('\n')]
    p1, p2 = 0, 0
    for update in updates:
        if update_rules.is_valid(update):
            p1 += update[len(update)//2]
        else:
            corrected_update = update_rules.sort(update)
            p2 += corrected_update[len(update)//2]
    return p1, p2


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


