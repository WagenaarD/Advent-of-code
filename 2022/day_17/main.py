"""
Advent of code challenge 2022
>> python3 main.py < in
Start   - 
Part 1  - 3181, ex 3068
Part 2  - 1570434782634 ex 1514285714288
Cleanup - 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function

ELEMENTS = (
    [int('0011110', 2)],
    [int('0001000', 2), int('0011100', 2), int('0001000', 2)],
    [int('0000100', 2), int('0000100', 2), int('0011100', 2)],
    [int('0010000', 2), int('0010000', 2), int('0010000', 2), int('0010000', 2)],
    [int('0011000', 2), int('0011000', 2)]
)
FULL_ROW = int('1111111', 2)
EMPTY_ROW = int('0000000', 2)


def print_chamber(chamber: list, elem: list = [], drop: int = 0) -> None:
    """
    Prints a representation of the current chamber. Using 10 drops of the exmample input gives:
      0. |....■..|
      1. |....■..|
      2. |....■■.|
      3. |■■..■■.|
      4. |■■■■■■.|
      5. |.■■■...|
      6. |..■....|
      7. |.■■■■..|
      8. |....■■.|
      9. |....■■.|
     10. |....■..|
     11. |..■.■..|
     12. |..■.■..|
     13. |■■■■■..|
     14. |..■■■..|
     15. |...■...|
     16. |..■■■■.|
         +-------+
    """
    for idx, line in enumerate(chamber[:-1]):
        output = '{:5}. '.format(idx if idx % 1 == 0 else '')
        output += '|{:07b}|'.format(line).replace('0', '.').replace('1', '■')
        if elem and 0 <= idx - drop < len(elem):
            output += ' <-- |{:07b}|'.format(elem[idx - drop]).replace('0', '.').replace('1', '■')
        print(output)
    print('       +{}+\n'.format('-' * 7))


def drop_one_element(chamber_int, elem_idx: int, jet_input: str):
    if (chamber_int, elem_idx, jet_input) in drop_one_element.cache:
        return drop_one_element.cache[(chamber_int, elem_idx, jet_input)]
    no_rows = len(format(chamber_int, 'b')) // 7
    chamber = [(chamber_int >> (7 * idx)) & FULL_ROW for idx in range(no_rows)]
    elem = ELEMENTS[elem_idx]
    chamber = [EMPTY_ROW for _ in range(len(elem)+3)] + chamber
    drop = 0
    jet_idx = 0
    # Simulate element motion
    while True:
        # first, simulate jet push
        jet_push = jet_input[jet_idx]
        jet_idx += 1
        # Either direction first tests wall-hit, then other-element-hit.
        if jet_push == '<':
            if not any([64 & el_row for el_row in elem]):
                if not any([(elem[idx] << 1) & chamber[idx + drop] for idx in range(len(elem))]):
                    elem = [el << 1 for el in elem]    
        else:
            if not any([1 & el_row for el_row in elem]):
                if not any([(elem[idx] >> 1) & chamber[idx + drop] for idx in range(len(elem))]):
                    elem = [el >> 1 for el in elem]
        # second, simulate downword motion
        down_hit = any([elem[idx] & chamber[idx + drop + 1] for idx in range(len(elem))])
        if any([elem[idx] & chamber[idx + drop + 1] for idx in range(len(elem))]):
            for idx, el in enumerate(elem):
                chamber[idx + drop] = chamber[idx + drop] | el
            break
        else:
            drop += 1
        if drop > len(chamber):
            raise(Exception('Infinite loop gaurd'))
    while chamber[0] == 0:
        chamber.pop(0)
    chamber, dropped_increment = reduce_chamber(chamber)
    output = (chamber, jet_idx, dropped_increment)
    drop_one_element.cache[(chamber_int, elem_idx, jet_input)] = output
    return output
drop_one_element.cache = {}


def reduce_chamber(chamber: list) -> tuple:
    """
    Reduces the chamber list by removing all all inaccessible elements and adding the removed rows
    to the score. This greatly reduces memory used and also reduced function call complexity for 
    drop_one_element. 

    All inaccessible rows are set to True, all accessible rows set to False. Non-bottom rows 
    consisting of only True are deleted and added to the score.

    Example, before:
      0. |.■.....|
      1. |■■■....|
      2. |.■■■■■.|
      3. |.■■■...|
      4. |.■■■...|
      5. |.■■■...|
      6. |.■■■.■.|
      7. |.■■■■■■|
      8. |.■■■■■■|
      9. |....■■■|
     10. |....■■■|
     11. |....■■■|
     12. |....■■■|
     13. |.■■.■■■|
     14. |.■■.■■■|
     15. |..■■■■■|
     16. |....■■■|
     17. |...■■■■|
     18. |■...■■■|
         +-------+

    Example, after (score incremented by 12)
      0. |.■.....|
      1. |■■■....|
      2. |■■■■■■.|
      3. |■■■■...|
      4. |■■■■...|
      5. |■■■■...|
      6. |■■■■.■.|
         +-------+
    """
    new_chamber = [FULL_ROW for _ in range(len(chamber))]
    stack = {(0, ~chamber[0] & (int('0000001', 2) << idx)) for idx in range(7)}
    while stack:
        row, col = stack.pop()
        new_chamber[row] -= col
        # To add a cell to the stack, it must:
        #  - not be out of bounds
        #  - be empty on the original chamber
        #  - be filled on the new chamber
        # It will then be cleared in new_chamber in a future loop
        for (dr, dc) in ((0, 1), (0, -1), (1, 0)):
            rr, cc = row + dr, col << dc if dc >0 else col >> -dc
            if not (rr > len(chamber) - 1 or cc == 0 or cc == 1 << 7):
                if ~chamber[rr] & cc:
                    if new_chamber[rr] & cc:
                        stack.add((rr, cc))
    dropped = 0
    while len(new_chamber) >= 2 and new_chamber[-2] == FULL_ROW:
        new_chamber.pop()
        dropped += 1
        
    return (new_chamber, dropped)


def simulate_element_drops(input: str, no_elements: int, reset_cache: int = 0) -> int:
    """
    Solves our Tetris problem for the supplied arguments. Input is a list of integers stored as a 
    big integer and needs to be unpacked. This speeds up caching.
    reset_cache can be set to detect patterns. If set to a value, the cache of drop_one_element will
    be reset once the value is reached and this will be stored as the start of the pattern. Letting
    the analysis run for longer then allows the detection of the length of the pattern.
    """
    chamber = [FULL_ROW]
    double_input = input * 2
    jet_idx = 0
    total_dropped = 0
    for elem_idx in range(no_elements):
        chamber, jet_increment, dropped_increment = drop_one_element(
            sum([line << 7 * idx for idx, line in enumerate(chamber)]),
            # chamber, 
            elem_idx % len(ELEMENTS), 
            double_input[jet_idx:jet_idx+33]
        )
        total_dropped += dropped_increment
        jet_idx = (jet_idx + jet_increment) % len(input)
        if reset_cache and len(drop_one_element.cache) >= reset_cache:
            drop_one_element.cache = {}
            get_score.pattern_start = elem_idx + 1

    return len(chamber) - 1 + total_dropped


def get_score(input: str, no_elements: int):
    """
    Uses the previously stored pattern to quickly calculate the output without simulating all 
    element drops. Only the remaining drops are simulated.
    """
    if get_score.pattern_start == None or get_score.pattern_len == None:
        return None
    if get_score.score_increase == None:
        get_score.score_increase = \
            simulate_element_drops(input, get_score.pattern_start + get_score.pattern_len) - \
            simulate_element_drops(input, get_score.pattern_start)
    if no_elements < get_score.pattern_start:
        return simulate_element_drops(input, no_elements)
    else:
        no_repetitions = (no_elements - get_score.pattern_start) // get_score.pattern_len
        return simulate_element_drops(input, no_elements - no_repetitions * get_score.pattern_len) + \
            no_repetitions * get_score.score_increase
get_score.score_increase = None
get_score.pattern_start = None
get_score.pattern_len = None


@print_function(run_time = True)
def solve(input):
    """
    The element drops follow a certain pattern. After about 2_000 simulations, all possible 
    calculations are already cached, but just looking up the answer still takes around 1E6s = 12 
    days. The simulation needs a while to set into the pattern and the start state is not part of 
    it. The trick here is to first run the simulation long enough to see how many unique states are
    encountered if the simulation is ran infinitively long. Next, we run the simulation again, but 
    detect after how many elements all states have been observed, this is the start of the pattern.
    If we then reset the cache and run the simulation long enough, the number of unique states is 
    the length of the pattern.

    Once the start and length of pattern are determined, the score per cycle is easily determined. 
    Once determined, the calculation of an arbitrary number of simulations is very fast as we only 
    need to calculate a up to the start of the pattern, then any full cycle can be skipped, and then
    the remainder partial cycle. Since all answers are already cahced this is very fast.
    """
    simulate_element_drops(input, 10_000)
    reset_cache = len(drop_one_element.cache)
    print('reset_cache', reset_cache)
    drop_one_element.cache = {}
    simulate_element_drops(input, 10_000, reset_cache = reset_cache)
    get_score.pattern_len = len(drop_one_element.cache)
    print('get_score.pattern_start', get_score.pattern_start)
    print('len(drop_one_element.cache)', len(drop_one_element.cache))
    print('Part 1:', get_score(input, 2022))
    print('Part 2:', get_score(input, 1_000_000_000_000))


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    solve(sys.stdin.read().strip())