"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import math
from collections import Counter

AOC_ANSWER = (105952, 975931446)

class UnionFind:
    def __init__(self, objects: list):
        self.parent = {obj: obj for obj in objects}
        self.no_groups = len(set(objects))
        """Dictionary storing an object's parent. If the parent is itself, there is no parent"""
    
    def find(self, object):
        """Finds the parent of the object. If the parent is multiple steps away, store the parent of 
        the parent"""
        if self.parent[object] == object:
            return object
        else:
            self.parent[object] = self.find(self.parent[object])
            return self.parent[object]

    def mix(self, child, parent):
        """
        Combine two objects by setting the parent of an object to the parent of another object
        """
        if self.find(child) != self.find(parent):
            self.no_groups -= 1
        # self.parent[child] = parent # THIS WAS THE BUG
        self.parent[self.find(child)] = self.find(parent)
    
    @property
    def groups(self):
        return len({self.find(obj) for obj in self.parent})
    
    @property
    def group_sizes(self):
        counter = Counter(self.find(obj) for obj in self.parent)
        return sorted(counter.values(), reverse = True)


def get_sq_dist(start: tuple[int, ...], end: tuple[int, ...]) -> int:
    """
    Calculates the square distance between two N-dimensional tuples. E.g. 
        (x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2
    """
    return sum((start_x - end_x)**2 for start_x, end_x in zip(start, end))


@print_function
def main(input_txt: str) -> tuple[int, int]:
    # Parse input
    boxes = [tuple(map(int, line.split(','))) for line in input_txt.split('\n')]
    if len(boxes) < 100:
        p1_cables = 10 # example input
    else:
        p1_cables = 1000
    # Calculate the cable distances
    distances = {}  
    for idx1, box1 in enumerate(boxes):
        for box2 in boxes[idx1+1:]:
            dist = get_sq_dist(box1, box2)
            assert dist not in distances, 'duplicate distances'
            distances[dist] = (box1, box2)
    # Loop over all cables
    union = UnionFind(boxes)
    score_p1, score_p2 = 0, 0
    for idx, dist in enumerate(sorted(distances), 1):
        box1, box2 = distances[dist]
        union.mix(box1, box2)
        # Part 1: After a number of cables, calculate the product of the largest three groups
        if idx == p1_cables:
            score_p1 = math.prod(val for val in union.group_sizes[:3])
        # Part 2: When all groups are combined, calculate the product of the last cable
        if union.no_groups == 1:
            score_p2 = box1[0] * box2[0]
        if score_p1 and score_p2:
            break
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
