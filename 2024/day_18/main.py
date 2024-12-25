"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, tuple_add
from collections import deque


AOC_ANSWER = (446, '39,40')
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def visualize(bytes: list[tuple[int, int]], width: int, height: int) -> None:
    """Prints the grid for the example input"""
    for r in range(height):
        row = []
        for c in range(width):
            row.append('#' if (r, c) in bytes else '.')
        print(''.join(row))


@print_function
def part_one(bytes: list[tuple[int, int]], width: int, height: int, step: int, is_example: bool) -> int:
    """Simple BFS to find the shortest path."""
    end = (height-1, width-1)
    qeue = deque([(0, (0, 0))])
    seen = set()
    walls = set(bytes[:step])
    while qeue:
        cost, pos = qeue.popleft()
        for dpos in DIRS:
            try:
                npos = tuple_add(pos, dpos)
            except:
                assert False

            if npos[0] in range(height) and npos[1] in range(width):
                if npos not in seen and npos not in walls:
                    if npos == end:
                        return cost+1
                    qeue.append((cost+1, npos))
                    seen.add(npos)
    return -1


@print_function
def part_two(bytes: list[tuple[int, int]], width: int, height: int) -> int:
    """
    Start by calculating all accessible locations when all blocks have fallen. Then remove them one 
    by one untill a path is visible. Each time a block is lifted, the set of accessible locations 
    from the last step is reused and expanded if the block is next to an accessible location. 
    """
    end = (height-1, width-1)
    seen = {(-1, 0)}
    bytes.append((0, 0))
    while end not in seen:
        last_byte = bytes.pop()
        for dpos in DIRS:
            if tuple_add(last_byte, dpos) in seen:
                seen.add(last_byte)
                break
        else:
            continue
        qeue = deque([last_byte])
        walls = set(bytes)
        while qeue:
            pos = qeue.popleft()
            for dpos in DIRS:
                npos = tuple_add(pos, dpos)
                if npos[0] in range(height) and npos[1] in range(width) and \
                        npos not in seen and npos not in walls:
                    qeue.append(npos)
                    seen.add(npos)
    return ','.join(map(str, reversed(last_byte)))

    
@print_function
def main(input_txt: str) -> tuple[int, int]:
    """Parses input then runs part one and two"""
    is_example = input_txt.count('\n') < 1000
    if input_txt.count('\n') < 1000:
        width, height, step = 7, 7, 12
    elif input_txt.count('\n') < 10_000:
        width, height, step = 71, 71, 1024
    else: # Extra input from reddit
        width, height, step = 213, 213, 1024
    bytes = []
    for line in input_txt.split('\n'):
        c, r = map(int, line.split(','))
        bytes.append((r, c))
    
    return (
        part_one(bytes, width, height, step, is_example), 
        part_two(bytes, width, height)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
