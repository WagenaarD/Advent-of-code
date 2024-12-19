"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
from functools import cache

AOC_ANSWER = (298, 572248688842069)

class DFS:
    """
    Class to handle DFS. Basically could have been a function, but I like to "store" the pattern in 
    the function somehow. I think a clear way of doing this is to create a class and store the 
    patterns in the class and then call cached functions (with only hashable arguments).
    """
    def __init__(self, patterns):
        self.patterns = patterns
    
    @cache
    def number_of_solutions(self, design: str) -> int:
        """Recursive function, determines how many ways the design can be created from patterns"""
        if design == '':
            return 1
        ans = 0
        for pattern in self.patterns:
            if design.startswith(pattern):
                ans += self.number_of_solutions(design.removeprefix(pattern))
        return ans
    

@print_function
def main(input_txt: str) -> tuple[int, int]:
    """Runs part 1 and part 2"""
    patterns_txt, designs_txt = input_txt.split('\n\n')
    dfs = DFS(patterns_txt.split(', '))
    possible_designs = [dfs.number_of_solutions(design) for design in designs_txt.split('\n')]
    return (
        sum(map(bool, possible_designs)),
        sum(possible_designs)
    )

aoc_run(__name__, __file__, main, AOC_ANSWER)


