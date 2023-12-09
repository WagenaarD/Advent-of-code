"""
Advent of code challenge 2022
>> python3 main.py < in
Part 1  - 1365 (ex 33)
Part 2  - 4864 (ex 3472) 
"""

import sys
sys.path.insert(0, '/'.join(__file__.replace('\\', '/').split('/')[:-2]))
from _utils.print_function import print_function
import re
from functools import cache
import math


# Optimization ideas:
#  x delta_t geode shortest -> always geode
#  x Never build more robots than the max. required for that resource
#  x Never build more robots than the robot cap. If none of the top scoring tracks include at least 
#      up to the cap amount of robots, quit.
#  x DIDNT WORK: If obsidian has the next-shortest dt, only consider it.
#  x DIDNT WORK: If obsidian has the next-shortest dt, only consider it or geode
#  x DIDNT WORK: If increasing the cap doesnt improve total_score, quit


def run_dfs(blueprint, tmax = 24):
    """
    Second attempt at DFS solution.
    Use a while loop instead of a recursive loop.
    - Con: No easy caching
    - Pro: Easier to keep track of overarching parameters

    Optimization ideas:
    - Don't assume the geode crusher always needs to be produced if possible, this is not always
    optimal
    - Calculate the max possible score and prune the tree if this is less than the already found
    highest score
    - The current highest score is the score of waiting out the rest of the time
    - The max. possible score is the score for buying a geode crusher on every turn after this one
    - The dfs prioritizes the paths buying expensive robots first, to help with this pruning
    - This works because a lot of buying decisions are concentrated in the last few minutes as a lot
    of resources are available then.
    """
    robot_cap = [max(bp[i] for bp in blueprint) for i in range(3)] + [tmax]
    stack = [(tmax, (1,0,0,0), (0,0,0,0))]
    output = []
    max_score = 0
    while stack:
        t, robots, resource = stack.pop()
        for rob in range(4):
            # Don't build more robots than allowed
            if robots[rob] >= robot_cap[rob]:
                continue
            required = blueprint[rob]
            dt = 1
            for res in range(3):
                # Test if we can already produce this
                if required[res] == 0: # should be <= resources[res]?
                    continue
                # Test if we produce this at all
                elif robots[res] == 0:
                    break
                # Calculate time to produce this
                else:
                    dt = max(dt, 1, 1 + math.ceil((required[res] - resource[res]) / robots[res]))
                    if dt >= t:
                        break
            else:
                cur_score = resource[3] + robots[3] * t + ((t - dt) if rob == 3 else 0)
                pot_score = cur_score + sum([i+1 for i in range((t - dt))])
                if pot_score < max_score:
                    continue
                max_score = max(cur_score, max_score)
                stack.append((
                    t - dt, 
                    tuple(robots[i] + (1 if i == rob else 0) for i in range(4)),
                    tuple(resource[i] + robots[i] * dt - blueprint[rob][i] for i in range(4))
                ))
        output.append(resource[3] + robots[3] * t)
    print('no_paths:', len(output))
    return max(output)


@print_function(run_time = True, include_args = False)
def solve_1(blueprints):
    total_q = 0
    for idx, blueprint in enumerate(blueprints):
        total_q += (idx + 1) * run_dfs(blueprint, 24)
    return total_q


@print_function(run_time = True, include_args = False)
def solve_2(blueprints):
    result = 1
    for blueprint in blueprints[0:3]:
        result *= run_dfs(blueprint, 32)
    return result


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    lines = sys.stdin.read().strip().split('\n')

    blueprints = []
    for line in lines:
        blueprint = []
        for robot in line.split('.')[:-1]:
            blueprint.append(tuple(map(int, (
                re.findall('(\d+) ore', robot)[0] if re.findall('(\d+) ore', robot) else 0,
                re.findall('(\d+) clay', robot)[0] if re.findall('(\d+) clay', robot) else 0,
                re.findall('(\d+) obsidian', robot)[0] if re.findall('(\d+) obsidian', robot) else 0,
                0,
            ))))
        blueprints.append(blueprint)

    solve_1(blueprints)
    solve_2(blueprints)
