"""
Advent of code challenge 2023
>> python3 main.py < in
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""
# Start, Part 1, Part 2
# 08:02:04
# 08:32:37
# 16:10:27

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
import re
from collections import namedtuple
SeedRange = namedtuple('SeedRange', ('start', 'end'))
LutRange = namedtuple('LutRange', ('start', 'end', 'offset'))

AOC_ANSWER = (309796150, 50716416)

def part_one(lines: list[str]) -> int:
    seeds = map(int, re.findall('\d+', lines[0]))
    luts = []
    for line in lines[1:]:
        if line == '':
            continue
        elif not line[0].isdigit():
            luts.append([])
        else:
            luts[-1].append([int(num) for num in re.findall('\d+', line)])
    p1 = []
    for pos in seeds:
        for lut in luts:
            for dst, src, lng in lut:
                if src <= pos < src + lng :
                    pos = dst + (pos - src)
                    break
        p1.append(pos)
    return min(p1)

def part_two(lines: list[str]) -> int:
    seed_ranges = [tuple(map(int, pair.split())) for pair in re.findall('\d+ \d+', lines[0])]
    seed_ranges = {SeedRange(start, start + length) for start, length in seed_ranges}

    map_lst = []
    for line in lines[1:]:
        if line == '':
            continue
        elif not line[0].isdigit():
            map_lst.append([])
        else:
            dst, lut_start, lut_len = map(int, re.findall('\d+', line))
            map_lst[-1].append(LutRange(lut_start, lut_start + lut_len, dst - lut_start))
    
    for luts in map_lst:
        lut_nodes = [lut.start for lut in luts] + [lut.end for lut in luts]
        next_seed_ranges = set()
        for seed_range in seed_ranges:
            nodes = sorted(list(set(lut_nodes + [seed_range.start, seed_range.end])))
            for node, next_node in zip(nodes, nodes[1:]):
                offset = 0
                if not (seed_range.start <= node < seed_range.end):
                    continue
                for lut in luts:
                    if lut.start <= node < lut.end:
                        offset = lut.offset
                        break
                next_seed_ranges.add(SeedRange(node + offset, next_node + offset - 1))
        seed_ranges = next_seed_ranges
    return min([num[0] for num in seed_ranges])
                

@print_function
def main(input: str) -> tuple[int, int]:
    lines = input.split('\n')
    return (part_one(lines), part_two(lines))

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')