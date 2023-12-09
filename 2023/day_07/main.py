"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 11:05:45
# 11:35:43
# 11:51:39

import sys
sys.path.append('..')
from aoc_tools import print_function
from collections import Counter

AOC_ANSWER = (250120186, 250665248)
HAND_RANKS = [[1,1,1,1,1], [2,1,1,1], [2,2,1], [3,1,1], [3,2], [4,1], [5]]
KICKER_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class Hand:
    def __init__(self, hand: str):
        self.hand: str = hand

    def strength(self, joker = '_') -> 'tuple(int, int, int, int, int, int)':
        kicker_rankings = [joker] + KICKER_RANKS
        joker_count = self.hand.count(joker)
        hand = self.hand.replace(joker, '')
        counts = sorted(Counter(hand).values(), reverse = True)
        if not counts: 
            # For edge case: hand = 'JJJJJ'
            counts = [0]
        counts[0] += joker_count
        strength = HAND_RANKS.index(counts)
        return (strength, *[kicker_rankings.index(card) for card in self.hand])
        

def solve(lines, joker = '_'):
    hand_list = [(Hand(hand), int(bid)) for hand, bid in [line.split() for line in lines]]
    hand_list.sort(key = lambda pair: pair[0].strength(joker))
    return sum([idx * bid for idx, (hand, bid) in enumerate(hand_list, 1)])


@print_function()
def main(input: str) -> 'tuple(int, int)':
    lines = input.split('\n')
    return (solve(lines), solve(lines, 'J'))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    input = sys.stdin.read().strip()
    print('  ->', main(input) == (AOC_ANSWER[0], AOC_ANSWER[1]))

