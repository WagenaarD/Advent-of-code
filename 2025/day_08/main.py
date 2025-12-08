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

AOC_ANSWER = (105952, 975931446)


def get_sq_dist(start: tuple[int, ...], end: tuple[int, ...]) -> int:
    """
    Calculates the square distance between two N-dimensional tuples. E.g. 
        (x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2
    """
    return sum((start_x - end_x)**2 for start_x, end_x in zip(start, end))


@print_function
def main(input_txt: str) -> tuple[int, int]:
    boxes = [tuple(map(int, line.split(','))) for line in input_txt.split('\n')]
    if len(boxes) < 100:
        number_of_cables = 10 # example input
    else:
        number_of_cables = 1000
    distances = {}  
    for idx1, box1 in enumerate(boxes):
        for box2 in boxes[idx1+1:]:
            dist = get_sq_dist(box1, box2)
            assert dist not in distances, 'duplicate distances'
            distances[dist] = (box1, box2)
    circuits = [{box} for box in boxes]
    for idx, dist in enumerate(sorted(distances)):
        # Consider one cable between box1 and box2
        box1, box2 = distances[dist]
        # Calculate the new list of circuits. The currect circuit connects box1, box2 and all 
        # circuits that were connected to either box1 or box2. This is combined with all circuits 
        # not connected with either box1 or box2
        new_circuits = []
        current_circuit = {box1, box2}
        for circuit in circuits:
            if box1 in circuit or box2 in circuit:
                current_circuit |=  circuit
            else:
                new_circuits.append(circuit)
        circuits = new_circuits + [current_circuit]
        # After a set number of cables (10 or 1000, depending on example or input), p1 is scored as 
        # the product of the size of the three largest circuits
        if idx + 1 == number_of_cables:
            circuits.sort(key = lambda circuit: len(circuit), reverse = True)
            score_p1 = math.prod(len(circuits[idx]) for idx in range(3))
        # Once a cable has connected all junctions boxes, p2 is scored by multiplying their 
        # x-positions
        if len(circuits) == 1:
            score_p2 = box1[0] * box2[0]
            break
    return score_p1, score_p2


aoc_run( __name__, __file__, main, AOC_ANSWER)
