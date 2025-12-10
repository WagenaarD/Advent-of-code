"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from aoc_tools import print_loop
from collections import defaultdict


AOC_ANSWER = (4759531084, 1539238860)


@print_function
def part_one(input_txt: str) -> int:
    corners = [tuple(map(int, line.split(','))) for line in input_txt.split('\n')]
    max_area = 0
    for idx, corner1 in enumerate(corners):
        for corner2 in corners[idx+1:]:
            area = (abs(corner1[0] - corner2[0]) + 1) * (abs(corner1[1] - corner2[1]) + 1)
            if area > max_area:
                # print(corner1, corner2, area)
                max_area = area
    return max_area


@print_function
def part_two(input_txt: str) -> int:
    """
    This likely is not-optimal but it got the right answer. It took ±0.8s with pypy and ±2s without.
    
    The code first stores the ranges for which each row (y-position) are inside or on the edge of 
    the ROI (i.e., red or green tiles). To speed this up, the code pre-computes a list of all 
    vertical paths are stored and a set y positions of corners.
    
    For each y-position, the code scans from left (lowest x) to right (highest x). When encountering 
    a vertical path or a └ or ┘ corner, the tiles are now inside. Also when any corner is 
    encountered the path is now along an edge. As long as the line is inside and/or along an edge, 
    all tiles are red/green. We store the ranges that are red-green for each y-position in the grid.
    
    In the next step, the code finds tests combinitions of corners and tests for 
    """
    corners = [tuple(map(int, line.split(','))) for line in input_txt.split('\n')]
    grid_x = range(min(c[0] for c in corners) - 1, max(c[0] for c in corners) + 2)
    grid_y = range(min(c[1] for c in corners) - 1, max(c[1] for c in corners) + 2)
    # Precompute vertical paths
    vertical = defaultdict(list)
    for cor1, cor2 in zip(corners, corners[1:] + [corners[0]]):
        if cor1[0] == cor2[0]:
            vertical[cor1[0]].append(range(min(cor1[1], cor2[1]), max(cor1[1], cor2[1]) + 1))
    # Precompute set of y_positions of corners
    corner_y_positions = {corner[1] for corner in corners}
    corners_by_y = {y: {corner[0] for corner in corners if corner[1] == y} for y in corner_y_positions}
    flipping_corners = {}
    # Precompute flipping corners: Flip in-rect for └ or ┘, not for ┌ or ┐ (the opposite would also 
    # work). The corner is an └ or ┘ corner if the maximum y of the surrounding corners is higher.
    for corner_prev, corner, corner_next in zip(corners, corners[1:] + corners[:1], corners[2:] + corners[:2]):
        flipping_corners[corner] = max(corner_prev[1], corner_next[1]) > corner[1]
    # Loop over all Y positions to assess which ranges of x contain red-green tiles for that row.
    redgreen_tile_ranges = {grid_y[0]: []}
    for y in print_loop(grid_y):
        # If there are no corners in this row, we can copy the last row. If this is the first row in 
        # the loop, use an empty range instead.
        if y not in corner_y_positions:
            continue
        # Track three properties:
        #  1. Are we currently inside the region of interest (roi). Tracking along the bottom line 
        #     of a contour also counts
        #  2. Are we currently tracking alongside a horizontal edge
        #  3. Are we currently on red/green tiles.
        redgreen_tile_ranges[y] =  []
        is_inside = False
        is_edge = False
        is_redgreen = False
        for x in grid_x:
            # Check whether there is a corner at this position. When encountering any corner, the 
            # is_edge property should flip. Also, for half of the corners, the is_inside property 
            # should flip.
            if y in corners_by_y and x in corners_by_y[y]:
                # Flip on-edge for any corner
                is_edge = not is_edge
                # Flip in-rect for └ or ┘
                if flipping_corners[(x, y)]:
                    is_inside = not is_inside
            # Flip for vertical paths!
            for r in vertical[x]:
                if y in r:
                    is_inside = not is_inside
            # When the cells flip from red/green to not red/green (or vice versa) store the range up
            # to that point. 
            if is_edge or is_inside:
                if not is_redgreen:
                    range_start = x
                    is_redgreen = True
            else:
                if is_redgreen:
                    redgreen_tile_ranges[y].append((range_start, x + 1))
                    is_redgreen = False
        assert not is_redgreen
    # Precompute the areas. This is relatively quick and this allows us to start investigating the 
    # largest areas first and stop once we found one which is entirely red/green.
    areas = []
    for idx, corner1 in enumerate(print_loop(corners)):
        for corner2 in corners[idx+1:]:
            min_corner = tuple(min(x, y) for x, y in zip(corner1, corner2))
            max_corner = tuple(max(x, y) for x, y in zip(corner1, corner2))
            area = (abs(corner1[0] - corner2[0]) + 1) * (abs(corner1[1] - corner2[1]) + 1)
            areas.append((area, min_corner[0], min_corner[1], max_corner[0], max_corner[1]))
    # Scan over each area in descending size. An area is valid if for every row there is a range 
    # which wraps around the x positions of the rectangle. To save time, we only scan unique rows
    # in the rectangle as well as the bottom row of the rectangle. We do not need to scan any others
    # as they are copies of the ones that precede it.
    areas.sort(reverse = True)
    unique_y = sorted(redgreen_tile_ranges)
    # For every rectangle
    for area, min_x, min_y, max_x, max_y in print_loop(areas):
        # for every y for which x_ranges of redgreen tiles are specified
        for idx, y in enumerate(unique_y):
            next_y = unique_y[(idx + 1) % len(unique_y)]
            # If the y is in the range of our rectangle, or its the y below our rectangle bottom
            if y <= min_y < next_y or min_y <= y <= max_y:
                # Check if there is a range which fits our rectangle X-domain
                for range_start, range_stop in redgreen_tile_ranges[y]:
                    if range_start <= min_x and max_x < range_stop:
                        # Row fits inside this specified range
                        break
                else:
                    # No fitting row was found -> Rectangle does not fit
                    break
        else:
            # Not broken out -> Rectangle fits
            return area


@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )


aoc_run( __name__, __file__, main, AOC_ANSWER)
