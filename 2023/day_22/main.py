"""
Advent of code challenge 2023
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in

Optimized with a little help (just like yesterday). My idea was to simulate gravity for all possible
missing blocks and score the amount of moving blocks. Easy to implement and took 90s to calculate.
A much better idea came from Reddit: Calculate which blocks lean on which. From there gravity no 
longer needs to be simulated.
"""
# Start, Part 1, Part 2
# 08:21:57
# 09:06:09
# 09:10:48
AOC_ANSWER = (477, 61555)

import sys
sys.path.append(AOC_BASE_PATH := '/'.join(__file__.replace('\\', '/').split('/')[:-3]))
from aoc_tools import print_function, aoc_run
from pprint import pprint
from collections import namedtuple
from functools import cache

Brick = namedtuple('Brick', ('min', 'max'))
Coord = namedtuple('Coord', ('x', 'y', 'z'))


@cache
def xy_collides(sx, sy, ex, ey, sxx, syy, exx, eyy):
    """
    sx, sy: lowest (starting) x and y of first brick
    ex, ey: highest (ending) x and y of first brick
    sxx, syy, exx, eyy: lowest and highest x and y of second brick
     |--------|
          |---------|
     sx  sxx  ex   exx
    The overlap (sxx-ex) is equal to the right-most starting point (max(sx, sxx)) to the left-most
    ending point (min(ex, exx)). If the overlap > 0, there is collission in the x direction.
    """
    return min(ex, exx) >= max(sx, sxx) and min(ey, eyy) >= max(sy, syy)
    

@print_function
def apply_gravity(bricks: list, only_count = False) -> int:
    bricks.sort(key=lambda b: b.min.z)
    moves = 0
    for idx, brick in enumerate(bricks):
        zz = 1
        for other in bricks[:idx]:
            if other.max.z >= brick.min.z:
                continue
            if not xy_collides(brick.min.x, brick.min.y, brick.max.x, brick.max.y, 
                               other.min.x, other.min.y, other.max.x, other.max.y):
                continue
            zz = max(zz, other.max.z + 1)
        assert zz <= brick.min.z, f'{idx=} {brick} {other}'
        if zz != brick.min.z:
            moves += 1
            bricks[idx] = Brick(
                Coord(brick.min.x, brick.min.y, zz), 
                Coord(brick.max.x, brick.max.y, zz + brick.max.z - brick.min.z),
            )
    return moves
 

@print_function
def main(input):
    lines = input.split('\n')
    bricks = []
    for line in lines:
        start, end = line.split('~')
        start = Coord(*map(int, start.split(',')))
        end = Coord(*map(int, end.split(',')))
        bricks.append(Brick(start, end))
        assert tuple(end) >= tuple(start), 'Start has lower values'
    apply_gravity(bricks)
    # make dict of which brick lean/support which brick
    leaning_on = {}
    supports = {}
    for brick in bricks:
        leaning_on[brick] = []
        supports[brick] = []
        for other in bricks:
            if other.max.z == brick.min.z - 1:
                if xy_collides(brick.min.x, brick.min.y, brick.max.x, brick.max.y, other.min.x, other.min.y, other.max.x, other.max.y):
                    supports[other].append(brick)
                    leaning_on[brick].append(other)
    # Score how many bricks move
    score_p1, score_p2 = 0, 0
    for brick in bricks:
        stack = {brick}
        moved = {brick}
        while stack:
            brick = stack.pop()
            for other in supports[brick]:
                if all(b in moved for b in leaning_on[other]):
                    stack.add(other)
                    moved.add(other)
        if len(moved) == 1:
            score_p1 += 1
        score_p2 += len(moved) - 1
    return score_p1, score_p2


aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')
# aoc_run(__name__, __file__, main, AOC_ANSWER, 'ex')


