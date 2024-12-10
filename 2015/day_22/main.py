"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (1824, 1937)

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

# Magic Missile costs 53 mana. It instantly does 4 damage.
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

MOVE_COSTS = {
    'Magic Missile': 53,
    'Drain': 73,
    'Shield': 113,
    'Poison': 173,
    'Recharge': 229,
}


def wizard_battle(input_txt: str, is_hard: bool = False) -> int:
    initial_player_hp, initial_player_mp, initial_boss_hp, boss_damage = map(int, re.findall('\\d+', input_txt))
    state = (initial_player_hp+boss_damage, initial_boss_hp, 0, initial_player_mp, 0, 0, 0, [])
    qeue = deque([state])
    lowest_cost = math.inf
    best_log = []
    debug = initial_player_hp == 10
    while qeue:
        player_hp, boss_hp, mp_spent, mp, shield_turns, poison_turns, recharge_turns, log = qeue.pop()
        
        # Start Boss's turn with status effects
        armor = 7 if shield_turns else 0
        if debug: log.append(f'\n-- Boss turn --\n- Player has {player_hp} hit points, {armor} armor, {mp} mana\n- Boss has {boss_hp} hit points.')
        if shield_turns:
            shield_turns -= 1
            if debug: log.append(f'Shield\'s timer is now 5 {shield_turns}.')
        if poison_turns:
            boss_hp -= 3
            poison_turns -= 1
            if debug: log.append(f'Poison deals 3 damage; its timer is now {poison_turns}.')
        if recharge_turns:
            mp += 101
            recharge_turns -= 1
            if debug: log.append(f'Recharge provides 101 mana; its timer is now {recharge_turns}.')
        
        # Process boss attack
        player_hp -= max(1, boss_damage - armor)
        if debug: log.append('Boss attacks for 8 damage.')

        # Start player's turn with status effects
        armor = 7 if shield_turns else 0
        if debug: log.append(f'\n-- Player turn --\n- Player has {player_hp} hit points, {armor} armor, {mp} mana\n- Boss has {boss_hp} hit points.')
        if shield_turns:
            shield_turns -= 1
            if debug: log.append(f'Shield\'s timer is now 5 {shield_turns}.')
        if poison_turns:
            boss_hp -= 3
            poison_turns -= 1
            if debug: log.append(f'Poison deals 3 damage; its timer is now {poison_turns}.')
        if recharge_turns:
            mp += 101
            recharge_turns -= 1
            if debug: log.append(f'Recharge provides 101 mana; its timer is now {recharge_turns}.')
        if is_hard:
            player_hp -= 1
            
        # Check win condition
        if mp_spent > lowest_cost:
            continue
        if boss_hp < 0:
            # print('!!' + str(mp_spent))
            lowest_cost = mp_spent
            best_log = log[:]
        if player_hp < 0:
            continue

        # Pick next move
        for move, move_cost in MOVE_COSTS.items():
            nlog = log + [f'Player casts {move}.']
            # Check if move can be cast
            if move_cost > mp:
                continue
            
            # Add move to the stack
            if move == 'Recharge':
                if recharge_turns:
                    continue
                else:
                    qeue.append((player_hp, boss_hp, mp_spent + move_cost, mp - move_cost, shield_turns, poison_turns, 5, nlog))
            elif move == 'Drain':
                qeue.append((player_hp+2, boss_hp-2, mp_spent + move_cost, mp - move_cost, shield_turns, poison_turns, recharge_turns, nlog))
            elif move == 'Shield':
                if shield_turns:
                    continue
                else:
                    qeue.append((player_hp, boss_hp, mp_spent + move_cost, mp - move_cost, 6, poison_turns, recharge_turns, nlog))
            elif move == 'Poison':
                if poison_turns:
                    continue
                else:
                    qeue.append((player_hp, boss_hp, mp_spent + move_cost, mp - move_cost, shield_turns, 6, recharge_turns, nlog))
            elif move == 'Magic Missile':
                qeue.append((player_hp, boss_hp-4, mp_spent + move_cost, mp - move_cost, shield_turns, poison_turns, recharge_turns, nlog))
        
    if debug: print('\n'.join(best_log[2:]))
    return lowest_cost


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        wizard_battle(input_txt), 
        wizard_battle(input_txt, True)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


