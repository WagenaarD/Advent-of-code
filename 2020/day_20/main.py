"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

AOC_ANSWER = (5775714912743, 1836)
from collections import namedtuple
MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

class Tile:
    num: int
    lines: list[str]
    tiles: list[str]
    edges: list[str]

    def __init__(self, num, lines):
        self.num = num
        self.lines = lines
        self.__update()

    def __update(self):
        top = self.lines[0]
        right = ''.join(line[-1] for line in self.lines)
        bottom = self.lines[-1][::-1]
        left = ''.join(line[0] for line in reversed(self.lines))
        self.edges = [top, right, bottom, left]
    
    @property
    def tiles(self):
        return [line[1:-1] for line in self.lines[1:-1]]

    def flip(self):
        """Flip horizontally"""
        self.lines = [l[::-1] for l in self.lines]
        self.__update()
    
    def rot(self):
        """Rotate by 90 deg clockwise"""
        self.lines = [''.join(self.lines[-1-r][c] \
                            for r in range(len(self.lines))) \
                            for c in range(len(self.lines[0]))]
        self.__update()
    
    def aligns(self, other: 'Tile') -> None | tuple[int, int]:
        """Returns the axis (if any) along which this tile aligns with another tile"""
        for idx in range(4):
            if self.edges[idx] == other.edges[(idx + 2) % 4][::-1]:
                return ((-1, 0), (0, 1), (1, 0), (0, -1))[idx]
    
    def __repr__(self):
        return f'Tile<{self.num}>'


@print_function
def main(input_txt: str) -> int:
    # parse input
    tiles = []
    for txt in input_txt.split('\n\n'):
        lines = txt.split('\n')
        num = int(re.findall('\\d+', lines.pop(0))[0])
        tiles.append(Tile(num, lines))
    # Find neighbours and add them to a grid
    tile = tiles[0]
    if True: # For example matching
        tile.flip()
        tile.rot()
        tile.rot()
    pos = (0, 0)
    stack: list[tuple[tuple[int, int], Tile]] = [(pos, tile)]
    grid: dict[tuple[int, int], Tile] = {pos: tile}
    while stack:
        pos, tile = stack.pop()
        for ntile in tiles:
            if ntile in grid.values():
                continue
            for _ in range(2):
                for _ in range(4):
                    aligns = tile.aligns(ntile)
                    if aligns:
                        dpos = aligns
                        npos = tuple(x + dx for x, dx in zip(pos, dpos))
                        grid[npos] = ntile
                        stack.append((npos, ntile))
                        break
                    ntile.rot()
                if ntile in grid.values():
                    break
                ntile.flip()
    # Convert grid dict to a nested list and calculate p1
    min_r = min(pos[0] for pos in grid)
    min_c = min(pos[1] for pos in grid)
    max_r = max(pos[0] for pos in grid)
    max_c = max(pos[1] for pos in grid)
    lgrid: list[list[Tile]] = []
    for r in range(min_r, max_r+1):
        lgrid.append([])
        for c in range(min_c, max_c+1):
            lgrid[-1].append(grid[(r, c)])
    score_p1 = lgrid[0][0].num * lgrid[0][-1].num * lgrid[-1][0].num * lgrid[-1][-1].num
    # Generate the true image
    image_lines = []
    for trow in lgrid:
        for lines in zip(*[tile.tiles for tile in trow]):
            image_lines.append(''.join(lines))
    # Interpret monster as a tile, then rotate and flip the monster. For each orientation, scan 
    # through the image for matches and overwrite these values.
    monster = Tile(-1, MONSTER.split('\n'))
    for flip_idx in range(2):
        for rot_idx in range(4):
            for row in range(len(image_lines)-len(monster.lines)+1):
                for col in range(len(image_lines[0])-len(monster.lines[0])+1):
                    # test for monster presence at this coordinate
                    matches = True
                    for mrow in range(len(monster.lines)):
                        for mcol in range(len(monster.lines[0])):
                            if monster.lines[mrow][mcol] == '#' and image_lines[row+mrow][col+mcol] not in '#O':
                                matches = False
                                break
                    if matches:
                        # print(f'Monster found. {flip_idx=}, {rot_idx=}, {row=}, {col=}, ')
                        for mrow in range(len(monster.lines)):
                            for mcol in range(len(monster.lines[0])):
                                nrow, ncol = row+mrow, col+mcol
                                if monster.lines[mrow][mcol] == '#':
                                    image_lines[nrow] = image_lines[nrow][:ncol] + 'O' + image_lines[nrow][ncol+1:]
            monster.rot()
        monster.flip()
    # print('\n'.join(image_lines))
    score_p2 = sum(line.count('#') for line in image_lines)
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
