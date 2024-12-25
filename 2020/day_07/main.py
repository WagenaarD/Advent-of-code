"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (300, 8030)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

SHINY_GOLD = 'shiny gold'

@print_function
def part_one(rules: dict) -> int:
    queue = list(rules.keys())
    has_gold = {SHINY_GOLD}
    queue.remove(SHINY_GOLD)
    while queue:
        for color in queue:
            if any(content_color in has_gold for content_color in rules[color]):
                has_gold.add(color)
                queue.remove(color)
                break
        else:
            break
    return len(has_gold) - 1

@print_function
def part_two(rules: dict) -> int:
    queue = list(rules.keys())
    number_of_bags = {}
    while queue:
        for color in queue:
            contents = rules[color]
            if all(content_color in number_of_bags for content_color in contents):
                number_of_bags[color] = 1
                for con_color, con_count in contents.items():
                    number_of_bags[color] += con_count * number_of_bags[con_color]
                if color == SHINY_GOLD:
                    return number_of_bags[SHINY_GOLD] - 1
                queue.remove(color)

@print_function
def main(input: str) -> tuple[int, int]:
    rules = {}
    for line in input.split('\n'):
        # Example input
        # light red bags contain 1 bright white bag, 2 muted yellow bags.
        container, rest = re.findall('(\\w+ \\w+) bags contain (.*)', line)[0]
        rules[container] = {key: int(val) for val, key in re.findall('(\\d+) (\\w+ \\w+) bag', rest)}
    return (
        part_one(rules), 
        part_two(rules)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


