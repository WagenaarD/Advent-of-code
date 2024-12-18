"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# Start, Part 1, Part 2

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run, Tup

AOC_ANSWER = (446, '39,40')
DIRS = list(map(Tup, [(-1, 0), (0, 1), (1, 0), (0, -1)]))

def visualize(bytes, width, height):
    """Prints the grid for the example input"""
    out = []
    for r in range(height):
        row = []
        for c in range(width):
            if Tup((r, c)) in bytes:
                row.append('#')
            else:
                row.append('.')
        out.append(''.join(row))
    out_txt = '\n'.join(out)
    print(out_txt)
    


@print_function
def part_one(input_txt: str) -> int:
    """
    Does a simple broad-first-search (BFS) to find the shortest path to the exit.
    """
    # Parse input
    is_example = input_txt.count('\n') < 1000
    if is_example:
        width, height, step = 7, 7, 12
    else:
        width, height, step = 71, 71, 1024
    bytes = []
    for line in input_txt.split('\n'):
        c, r = map(int, line.split(','))
        bytes.append(Tup((r, c)))
    if is_example: visualize(bytes[:step], width, height)
    # Start BFS
    end = Tup((height-1, width-1))
    qeue = [(0, Tup((0, 0)))]
    seen = set()
    walls = set(bytes[:step])
    while qeue:
        cost, pos = qeue.pop(0)
        for dpos in DIRS:
            npos = pos + dpos
            if npos[0] in range(height) and npos[1] in range(width):
                if npos not in seen and npos not in walls:
                    if npos == end:
                        return cost+1
                    qeue.append((cost+1, npos))
                    seen.add(npos)
    return None


@print_function
def part_two(input_txt: str) -> int:
    """
    Start by calculating all accessible locations when all blocks have fallen. Then remove them one 
    by one untill a path is visible. Each time a block is lifted, the set of accessible locations 
    from the last step is reused and expanded if the block is next to an accessible location. 
    """
    # Parse input
    is_example = input_txt.count('\n') < 1000
    if is_example:
        width, height = 7, 7
    else:
        width, height = 71, 71
    bytes = []
    for line in input_txt.split('\n'):
        c, r = map(int, line.split(','))
        bytes.append(Tup((r, c)))
    # Prepare our BFS
    end = Tup((height-1, width-1))
    seen = {Tup((-1, 0))}
    bytes.append(Tup((0, 0)))
    # Remove one wall at a time untill we find a path
    while end not in seen:
        last_byte = bytes.pop()
        for dpos in DIRS:
            if last_byte + dpos in seen:
                seen.add(last_byte)
                break
        else:
            continue
        qeue = [last_byte]
        walls = set(bytes)
        while qeue:
            pos = qeue.pop(0)
            for dpos in DIRS:
                npos = pos + dpos
                if npos[0] in range(height) and npos[1] in range(width) and \
                        npos not in seen and npos not in walls:
                    qeue.append(npos)
                    seen.add(npos)
    return ','.join(map(str, reversed(last_byte)))

    
@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


