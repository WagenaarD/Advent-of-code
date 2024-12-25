"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2

AOC_ANSWER = (956, 40149)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import cache


class Circuit:
    def __init__(self, lines):
        self.defs = {}
        for line in lines:
            lside, rside = line.split(' -> ')
            self.defs[rside] = lside
        self.idx = 0

    @cache
    def __getitem__(self, key: str):
        """Overrides the Circuit[key] operator"""
        assert type(key) == str
        if key.isdigit():
            return int(key)
        definition = self.defs[key]
        assert type(definition) == str
        if (op := ' AND ') in definition:
            key1, key2 = definition.split(op)
            return self[key1] & self[key2]
        elif (op := ' OR ') in definition:
            key1, key2 = definition.split(op)
            return self[key1] | self[key2]
        elif (op := ' LSHIFT ') in definition:
            key1, key2 = definition.split(op)
            return self[key1] << self[key2]
        elif (op := ' RSHIFT ') in definition:
            key1, key2 = definition.split(op)
            return self[key1] >> self[key2]
        elif (op := 'NOT ') in definition:
            key = definition.split(op)[1]
            return ~self[key]
        elif definition.isdigit():
            return int(definition)
        else:
            return self[definition]


@print_function
def main(input: str) -> tuple[int, int]:
    circuit = Circuit(input.split('\n'))
    p1 = circuit['a']
    circuit = Circuit(input.split('\n'))
    circuit.defs['b'] = str(p1)
    p2 = circuit['a']
    return p1, p2
    
    

aoc_run( __name__, __file__, main, AOC_ANSWER, 'in')


