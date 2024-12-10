"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (111, 188)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache, reduce
import math
from pprint import pprint

# Weapons:    Cost  Damage  Armor
WEAPONS_TXT = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0""".strip()

# Armor:      Cost  Damage  Armor
ARMOR_TXT = """
NoArmor       0     0       0 
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5""".strip()

# Rings:      Cost  Damage  Armor
RINGS_TXT = """
Damage_+1    25     1       0
Damage_+2    50     2       0
Damage_+3   100     3       0
Defense_+1   20     0       1
Defense_+2   40     0       2
Defense_+3   80     0       3""".strip()


@print_function
def main(input_txt: str) -> tuple[int, int]:
    boss_initial_hp, boss_damage, boss_armor = map(int, re.findall('\\d+', input_txt))
    weapons = {line.split()[0]: list(map(int, line.split()[1:])) for line in WEAPONS_TXT.split('\n')}
    armors = {line.split()[0]: list(map(int, line.split()[1:])) for line in ARMOR_TXT.split('\n')}
    rings = {line.split()[0]: list(map(int, line.split()[1:])) for line in RINGS_TXT.split('\n')}
    
    # Try all possible gear combinations
    lowest_cost = math.inf
    highest_cost = 0
    for weapon_specs in weapons.values():
        for armor_specs in armors.values():
            for no_rings in range(3):
                for ring_names in it.permutations(rings, no_rings):
                    # Calculate the relevant specs
                    gear = [weapon_specs, armor_specs] + [rings[name] for name in ring_names]
                    player_armor = sum(spec[2] for spec in gear)
                    player_damage = sum(spec[1] for spec in gear)
                    gold_spent = sum(spec[0] for spec in gear)
                    player_hp = 100
                    boss_hp = boss_initial_hp

                    # start simulation
                    while boss_hp > 0 and player_hp > 0:
                        boss_hp -= max(1, player_damage - boss_armor)
                        player_hp -= max(1, boss_damage - player_armor)
                    player_wins = boss_hp <= 0
                    
                    # Store result
                    if not player_wins and gold_spent > highest_cost:
                        highest_cost = gold_spent
                    if player_wins and gold_spent < lowest_cost:
                        lowest_cost = gold_spent
    return lowest_cost, highest_cost


aoc_run(__name__, __file__, main, AOC_ANSWER)


