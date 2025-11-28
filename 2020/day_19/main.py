"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (120, 350)


@print_function
def solve(input_txt: str, part_2 = False) -> int:
    """
    In part 2, two rules are overwritten:
        8: 42 | 42 8
        11: 42 31 | 42 11 31
    This generates a recursive problem which I don't try to solve. 8 is easily replaced with 42+ and
    11 is replaced by 42{n}31{n} for any n ≥ 1. I estimated the max number of n based on the largest
    message and the minimal combined length of 42 and 31. Basd on this, the pattern is generated for
    enough repititions e.g., (42.31)|(42{2}.31{2})|(42{3}.31{3})|(42{4}.31{4})... etc.
    """
    # Parse the rules and store them as a dict
    rules_txt, messages_txt = input_txt.split('\n\n')
    rules = dict()
    for rule_txt in rules_txt.split('\n'):
        key, definiton = rule_txt.split(': ')
        if definiton[0] == '"':
            rules[key] = [[definiton[1]]]
        else:
            rules[key] = [el.split(' ') for el in definiton.split(' | ')]
    if part_2:
        rules['8'] = [['42'], ['42', '8']]
        rules['11'] = [['42', '31'], ['42', '11', '31']]

    # Simplify rules to regex patterns. Two rules consist of only a and b. Then, the code looks for 
    # rules expressed only in rules expressed in ab and adds them to the list. Ultimately, all rules
    # are stored as a regex pattern.
    # For part 2, the minimum length of the pattern is stored and two rules are handled manually as
    # they involve a recursive pattern
    rule_pattern = {key: val[0][0][0] for key, val in rules.items() if val[0][0][0] in 'ab' }
    rule_min_length = {key: 1 for key in rule_pattern}
    max_len = max(len(message) for message in messages_txt.split('\n'))
    while True:
        for key, definition in rules.items():
            if key in rule_pattern:
                continue
            # Handle special p2 case 8
            if part_2 and '42' in rule_pattern and '8' not in rule_pattern:
                rule_pattern['8'] = f'({rule_pattern["42"]})+'
                rule_min_length['8'] = rule_min_length['42']
                continue
            # Handle special p2 case 11
            if part_2 and '42' in rule_pattern and '31' in rule_pattern and '11' not in rule_pattern:
                rule_pattern['11'] = f'(({rule_pattern["42"]})({rule_pattern["31"]})'
                max_repetition = max_len // (rule_min_length["42"] + rule_min_length["31"])
                for idx in range(1, max_repetition + 1):
                    rep = '{' + str(idx) + '}'
                    rule_pattern['11'] += '|' + f'(({rule_pattern["42"]}){rep})(({rule_pattern["31"]}){rep})'
                rule_pattern['11'] += ')'
                rule_min_length['11'] = rule_min_length['42'] + rule_min_length['31']

            flat_definition = [elem for sub_definition in definition for elem in sub_definition]
            if not all(elem in rule_pattern for elem in flat_definition):
                continue
            new_pattern_list = []
            min_lengths = []
            for sub_def in definition:
                min_lengths.append(sum(rule_min_length[elem] for elem in sub_def))
                new_pattern_list.append('(' + ''.join(f'({rule_pattern[elem]})' for elem in sub_def) + ')')
            rule_pattern[key] = '|'.join(new_pattern_list)
            rule_min_length[key] = min(min_lengths)
            break
        else:
            break

    # Do the scoring. Adding all messages that match rule '0'
    score = 0
    for message in messages_txt.split('\n'):
        matches_0 = bool(re.fullmatch(rule_pattern['0'], message))
        score += matches_0
    return score

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        solve(input_txt, False), 
        solve(input_txt, True)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
