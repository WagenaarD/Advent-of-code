import sys
from pathlib import Path
import itertools as it
from functools import cmp_to_key
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run

AOC_ANSWER = (6041, 4884)

## ORIGINE OPLOSSING
class UpdateRules:
    """
    A class to parse and enforce update rules for sorting.
    
    Args:
        rules_txt (str): Rules in the format "num1|num2". `True` means `num1` must come before `num2`.
    """

    def __init__(self, rules_txt: str):
        self.rules: dict[tuple[int, int], bool] = {}
        for line in rules_txt.splitlines():
            num1, num2 = map(int, line.split('|'))
            self.rules[(num1, num2)] = True
            self.rules[(num2, num1)] = False

    def is_valid(self, update: list[int]) -> bool:
        """Check if a list of updates satisfies all rules."""
        return all(
            self.rules.get(pair, True) for pair in it.combinations(update, 2)
        )

    def sort(self, update: list[int]) -> list[int]:
        """Sort the update list iteratively to satisfy all rules."""
        while True:
            for nums in it.combinations(update, 2):
                if nums in self.rules and not self.rules[nums]:
                    idxs = [update.index(num) for num in nums]
                    update[idxs[0]], update[idxs[1]] = update[idxs[1]], update[idxs[0]]
                    break
            else:
                return update

@print_function
def main(input: str) -> tuple[int, int]:
    rules_txt, updates_txt = input.split('\n\n')
    update_rules = UpdateRules(rules_txt)
    updates = [list(map(int, line.split(','))) for line in updates_txt.splitlines()]
    
    def get_middle_element(lst: list[int]) -> int:
        return lst[len(lst) // 2]

    p1, p2 = 0, 0
    for update in updates:
        if update_rules.is_valid(update):
            p1 += get_middle_element(update)
        else:
            corrected_update = update_rules.sort(update)
            p2 += get_middle_element(corrected_update)

    return p1, p2

## AANGEPASTE OPLOSSING
@print_function
def main(input: str) -> tuple[int, int]:
    rules_txt, updates_txt = input.split('\n\n')
    comp = lambda x, y, rules_txt=rules_txt: -(f'{x}|{y}' in rules_txt)
    get_middle_element = lambda lst: int(lst[len(lst)//2])
    p1, p2 = 0, 0
    for line in updates_txt.splitlines():
        update = line.split(',')
        sorted_update = sorted(update, key=cmp_to_key(comp))
        if update == sorted_update:
            p1 += get_middle_element(update)
        else:
            p2 += get_middle_element(sorted_update)
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
