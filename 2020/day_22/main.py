"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop, tuple_add, tuple_sub, tuple_mult, Pos
import itertools as it
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import re
import numpy as np
from pprint import pprint
from functools import cache, reduce
import math
from pprint import pprint
import heapq

AOC_ANSWER = (33421, 33651)

def score_deck(deck):
    return sum(idx * card for idx, card in enumerate(reversed(deck), 1))

@print_function
def part_one(input_txt: str, log: bool = False) -> int:
    p1_txt, p2_txt = input_txt.split('\n\n')
    deck_p1 = list(map(int, p1_txt.split('\n')[1:]))
    deck_p2 = list(map(int, p2_txt.split('\n')[1:]))
    round_idx = 0
    while deck_p1 and deck_p2:
        round_idx += 1 
        if log:
            print(f'\n -- Round {round_idx} --')
            print(f'Player 1\'s deck: {", ".join(str(c) for c in deck_p1)}')
            print(f'Player 2\'s deck: {", ".join(str(c) for c in deck_p2)}')
            print(f'Player 1 plays: {deck_p1[0]}')
            print(f'Player 2 plays: {deck_p2[0]}')
            print(f'Player {1+(deck_p1[0]<deck_p2[0])} wins the round!')
        if deck_p1[0] > deck_p2[0]:
            deck_p1.append(deck_p1.pop(0))
            deck_p1.append(deck_p2.pop(0))
        else:
            deck_p2.append(deck_p2.pop(0))
            deck_p2.append(deck_p1.pop(0))
    if log:
        print(f'\n == Post-game results ==')
        print(f'Player 1\'s deck: {", ".join(str(c) for c in deck_p1)}')
        print(f'Player 2\'s deck: {", ".join(str(c) for c in deck_p2)}')
    score_p1 = sum(idx * card for idx, card in enumerate(reversed(deck_p1 + deck_p2), 1))
    return score_p1


@cache
def game(decks: tuple[tuple[int], tuple[int]]) -> tuple[bool, tuple[tuple[int], tuple[int]]]:
    """
    Simulates a single game of recursive crab combat.
    """
    seen = set()
    while True:
        # Before either player deals a card, if there was a previous round in this game that had 
        # exactly the same cards in the same order in the same players' decks, the game instantly 
        # ends in a win for player 1. Previous rounds from other games are not considered. (This 
        # prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
        if decks in seen:
            # p1 wins: False
            return False, decks
        seen.add(decks)
        # The players begin the round by each drawing the top card of their deck as normal.
        cards = (decks[0][0], decks[1][0])
        decks = (decks[0][1:], decks[1][1:])
        if len(decks[0]) >= cards[0] and len(decks[1]) >= cards[1]:
            # If both players have at least as many cards remaining in their deck as the value of 
            # the card they just drew, the winner of the round is determined by playing a new game 
            # of Recursive Combat.
            winner, _ = game((decks[0][:cards[0]], decks[1][:cards[1]]))
        else:
            # Otherwise, at least one player must not have enough cards left in their deck to 
            # recurse; the winner of the round is the player with the higher-value card.
            winner = cards[1] > cards[0]
        # The winner of the round (even if they won the round by winning a sub-game) takes the two 
        # cards dealt at the beginning of the round and places them on the bottom of their own deck 
        # (again so that the winner's card is above the other card).
        # True means p2 won, False means p1 won.
        if winner: 
            #p2 won
            decks = (
                decks[0],
                decks[1] + (cards[1], cards[0]),
            )
        else:
            # p1 won
            decks = (
                decks[0] + (cards[0], cards[1]),
                decks[1],
            )
        # If a player has no deck left, the other player wins.
        if not decks[0]:
            # p1 deck empty, p2 wins: True
            return True, decks
        if not decks[1]:
            # p2 deck empty, p1 wins: False
            return False, decks    


@print_function
def part_two(input_txt: str) -> int:
    decks = tuple(tuple(map(int, txt.split('\n')[1:])) for txt in input_txt.split('\n\n'))
    _, decks = game(decks)
    return score_deck(decks[0] + decks[1])
    

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
