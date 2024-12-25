"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4580, ez 64
Part 2  - 2610, ex 58
Cleanup - 
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (4580, 2610)

class InsideBfs:
    def __init__(self, drops: list):
        self.drops = drops
        self.min_bound = tuple(min([d[ax] for d in drops]) - 1 for ax in range(3))
        self.max_bound = tuple(max([d[ax] for d in drops]) + 1 for ax in range(3))
        self.outside = set()
        self.update()
    

    def out_of_bounds(self, coord: tuple) -> bool:
        return any([coord[ax] < self.min_bound[ax] or coord[ax] > self.max_bound[ax] \
                        for ax in range(3)])
    

    def update(self):
        seen = set()
        # stack = {(self.min_bound[ax], self.min_bound, self.min_bound)}
        stack = {tuple(self.min_bound[ax] for ax in range(3))}
        while stack:
            coord = stack.pop()
            seen.add(coord)
            for dir in ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)):
                new_coord = tuple(coord[ax] + dir[ax] for ax in range(3))
                if not new_coord in self.drops and \
                        not new_coord in seen and \
                        not self.out_of_bounds(new_coord):    
                    stack.add(new_coord)
        self.outside = seen


    def test(self, coord: tuple, pockets_inside: bool = True) -> bool:
        if pockets_inside:
            return not self.out_of_bounds(coord) and not coord in self.outside
        else:
            return coord in self.drops


@print_function
def main(input_txt: str) -> tuple[int, int]:
    lines = input_txt.split('\n')
    drops = [tuple(map(int, re.findall('[0-9]+', line))) for line in lines]
    inside = InsideBfs(drops)

    ans = tuple()
    for part in (False, True):
        faces = 0
        for x in range(inside.min_bound[0], inside.max_bound[0] + 1):
            for y in range(inside.min_bound[1], inside.max_bound[1] + 1):
                for z in range(inside.min_bound[2], inside.max_bound[2] + 1):
                    in_drop = inside.test((x, y, z), part)
                    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                        faces += in_drop != inside.test((x + dx, y + dy, z + dz), part)
        ans = ans + (faces,)
        # print('Part {}:'.format(int(part)), faces)
    return ans

aoc_run(__name__, __file__, main, AOC_ANSWER)
