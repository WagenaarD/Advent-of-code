"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 4580, ez 64
Part 2  - 2610, ex 58
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import re


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


@print_function(run_time = True)
def solve(lines):
    drops = [tuple(map(int, re.findall('[0-9]+', line))) for line in lines]
    inside = InsideBfs(drops)

    for part in (False, True):
        faces = 0
        for x in range(inside.min_bound[0], inside.max_bound[0] + 1):
            for y in range(inside.min_bound[1], inside.max_bound[1] + 1):
                for z in range(inside.min_bound[2], inside.max_bound[2] + 1):
                    in_drop = inside.test((x, y, z), part)
                    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                        faces += in_drop != inside.test((x + dx, y + dy, z + dz), part)
        print('Part {}:'.format(int(part)), faces)
    

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""

    lines = sys.stdin.read().strip().split('\n')
    solve(lines)
