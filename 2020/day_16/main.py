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
from pprint import pprint
from pprint import pprint

AOC_ANSWER = (26869, 855275529001)


@print_function
def main(input_txt: str) -> int:
    input_parts = input_txt.split('\n\n')
    class_ranges = {}
    
    # Parse the class range definitions
    for range_txt in input_parts[0].split('\n'):
        range_name = range_txt[:range_txt.find(':')]
        class_ranges[range_name] = list(map(int, re.findall('\\d+', range_txt)))
    my_ticket_numbers = list(map(int, input_parts[1].split('\n')[1].split(',')))
    
    # Check which tickets are valid (p1)
    nearby_tickets = [list(map(int, line.split(','))) for line in input_parts[2].split('\n')[1:]]
    score_p1 = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for num in ticket:
            for lower_1, upper_1, lower_2, upper_2 in class_ranges.values():
                if lower_1 <= num <= upper_1 or lower_2 <= num <= upper_2:
                    # invalid num
                    break
            else:
                # invalid num
                is_valid = False
                score_p1 += num
        if is_valid:
            valid_tickets.append(ticket)
    
    # Get the possible class positions (p2.1)
    possible_class_positions = {key: list(range(len(my_ticket_numbers))) for key in class_ranges}
    for ticket in valid_tickets:
        for idx, num in enumerate(ticket):
            for class_name, (lower_1, upper_1, lower_2, upper_2) in class_ranges.items():
                if not (lower_1 <= num <= upper_1 or lower_2 <= num <= upper_2):
                        possible_class_positions[class_name].remove(idx)
    
    # Find the correct order of class positions (p2.2)
    my_ticket_values = {}
    while possible_class_positions:
        for class_name, idx_options in possible_class_positions.items():
            if len(idx_options) != 1:
                continue
            idx = idx_options[0]
            my_ticket_values[class_name] = my_ticket_numbers[idx]
            possible_class_positions.pop(class_name)
            for remaining_options_list in possible_class_positions.values():
                if idx in remaining_options_list:
                    remaining_options_list.remove(idx)
            break

    # scoring p2
    score_p2 = 1
    for class_name, value in my_ticket_values.items():
        if class_name.startswith('departure'):
            score_p2 *= value
        
    return score_p1, score_p2

aoc_run( __name__, __file__, main, AOC_ANSWER)
