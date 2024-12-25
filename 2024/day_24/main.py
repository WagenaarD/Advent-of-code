"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it

AOC_ANSWER = (38869984335432, 'drg,gvw,jbp,jgc,qjb,z15,z22,z35')

def process_gates(reg: dict[str, int], gates: list[str]) -> dict[str, int]:
    reg = reg.copy()
    old_reg = {}
    while reg != old_reg:
        old_reg = reg.copy()
        for line in gates:
            key1, cmd, key2, _, target = line.split(' ')
            if key1 not in reg or key2 not in reg:
                continue
            match cmd:
                case 'AND':
                    reg[target] = reg[key1] and reg[key2]
                case 'OR':
                    reg[target] = reg[key1] or reg[key2]
                case 'XOR':
                    reg[target] = not (reg[key1] == reg[key2])
    return reg

def get_xyz(reg, max_z = None):
    x, y, z = 0, 0, 0
    for idx in it.count():
        if max_z is not None and idx > max_z:
            break
        if (key := f'x{idx:02}') in reg:
            x += reg[key] << idx
        if (key := f'y{idx:02}') in reg:
            y += reg[key] << idx
        if (key := f'z{idx:02}') in reg:
            z += reg[key] << idx
        else:
            break
    return x, y, z


@print_function
def part_one(input_txt: str) -> int:
    """
    Find the int value for z for a given set of x and y values and operators.
    """
    initial_txt, gates_txt = input_txt.split('\n\n')
    reg = {line[:3]: int(line[-1]) for line in initial_txt.split('\n')}
    gates = gates_txt.split('\n')
    reg = process_gates(reg, gates)
    return get_xyz(reg)[2]

def find_one_error(gates: dict[tuple, str]) -> tuple[str, str]:
    """
    Finds the next wrongly connected logic gate. We simulate a binary addition logic circuit where
    z = x + y and x00 is the first bit (1) x01 the second (2) and xnn is the nth bit (2**(n-1)).

    For z00, we get:
    y00      x00
     │        │
     │        └───┬───────┐
     │            │      XOR ─── z00
     └─────────┬──────────┘
               │  │
               │  └───────┐
               │         AND ─── a01 (carried out)
               └──────────┘

    For z01 (and later ones), the circuit is slightly more complex:
    y01      x01            a01 (carried in)
     │        │              └────┬───┐
     │        └───────┬───┐       │  XOR ─── z01
     │                │  XOR ─┬───────┘ (← b01)
     └──────────────┬─────┘   │   └───┐
                    │ └───┐   │      AND ──┐ (← c01)
                    │    AND┐ └───────┘    │
                    └─────┘ │   (↓ d01)    OR ── a02 (carried out)
                            └──────────────┘


    We can simulate the logic circuit to find where the layout is erroneous. For my input it was
    enough to keep a set of A and B variable names (these are used as input for AND and XOR gates)
    and C and D variables (used as input for OR gates). We can determine the variabele names of A,
    B, C and D for increasing bits and verify that these

    """
    # Define some helper variables
    inv_gates = {val: key for key, val in gates.items()}
    ab_combinations = set()
    cd_combinations = set()
    pairs = {}
    for k1, cmd, k2 in gates:
        pairs[k1] = k2
        pairs[k2] = k1
        if cmd in ('AND', 'XOR'):
            ab_combinations.update({k1, k2})
        if cmd == 'OR':
            cd_combinations.update({k1, k2})
    # Check a special case, z00 is determined using only x00 and y00
    key = ('x00', 'XOR', 'y00')
    if gates[key] != 'z00':
        print('    gates[key] != \'z00\'')
        return (gates[key], 'z00')
    # All other cases should have 4 operations
    a_key = ('x00', 'AND', 'y00')
    a_name = gates[a_key]
    for idx in range(1, 45):
        x_name, y_name, z_name = (f'{axis}{idx:02}' for axis in 'xyz')
        b_name = gates[(x_name, 'XOR', y_name)]
        if a_name not in ab_combinations or b_name not in ab_combinations:
            # Both A and B should be in ab_combinations.
            print('    a_name not in ab_combinations or b_name not in ab_combinations')
            correct = b_name if a_name not in ab_combinations else a_name
            wrong = a_name if a_name not in ab_combinations else b_name
            return (wrong, pairs[correct])
        if a_name != pairs[b_name]:
            # If A and B are not supposed to be together, we can find the correct one by finding 
            # the gate that points to z.
            key = inv_gates[z_name]
            correct = a_name if a_name in key else b_name
            wrong = b_name if a_name in key else a_name
            return (wrong, pairs[correct])
        z_key = gkey(a_name, b_name, 'XOR')
        d_key = gkey(a_name, b_name, 'AND')
        if gates[z_key] != z_name:
            # Output of z is incorrect, swap with the actual z value
            print('    gates[z_key] != z_name')
            return (gates[z_key], z_name)
        c_name = gates[gkey(x_name, y_name, 'AND')]
        d_name = gates[d_key]
        if c_name not in cd_combinations or d_name not in cd_combinations:
            # Both C and D should be in cd_combinations.
            print('    c_name not in cd_combinations or d_name not in cd_combinations')
            correct = d_name if c_name not in cd_combinations else c_name
            wrong = c_name if c_name not in cd_combinations else d_name
            return (wrong, pairs[correct])
        if c_name != pairs[d_name]:
            # Backtrack from the next Z. 
            next_z_name = f'z{idx+1:02}'
            k1, _, k2 = inv_gates[next_z_name]
            for var_name in (k1, k2):
                key = inv_gates[var_name]
                if 'OR' in key:
                    correct = c_name if c_name in key else d_name
                    wrong = d_name if c_name in key else c_name
                    return (wrong, pairs[correct])
            assert False
        a_key = gkey(c_name, d_name, 'OR')
        a_name = gates[a_key]
        if idx == 44 and a_name != 'z45':
            print('    idx == 44 and a_name != \'z45\'')
            return ('z45', a_name)
    print('    None')
    return None

def gkey(key1, key2, command):
    """Provides a dictionary key that does not depend on key1 and key2 ordering"""
    return (min(key1, key2), command, max(key1, key2))

@print_function
def part_two(input_txt: str) -> int:
    """
    Looks for errors and fixes them. After four times the logic should be correct.
    """
    gates = {}
    for line in input_txt.split('\n\n')[1].split('\n'):
        key1, cmd, key2, _, target = line.split(' ')
        key1, key2 = sorted((key1, key2))
        gates[(key1, cmd, key2)] = target
    inv_gates = {val: key for key, val in gates.items()}
    swapped_outputs = []
    for idx in range(6):
        ans = find_one_error(gates)
        if ans == None:
            break
        key1, key2 = ans
        print(f'Swap found:')
        print(f'  gates[{inv_gates[key1]}] ≠ {key1}')
        print(f'  gates[{inv_gates[key2]}] ≠ {key2}')
        swapped_outputs.extend([key1, key2])
        gates[inv_gates[key1]], gates[inv_gates[key2]] = key2, key1
    else:
        raise(Exception(f'Reached maximum number of fixes after {idx+1} iterations'))
    return ','.join(map(str, sorted(swapped_outputs)))


codes = {}
inv_codes = {}
def test(input_txt):
    """
    Our input did not contain all types of swaps, so in this function we test if our code can detect
    all types of swaps by first fixing the code and then adding all possible swaps and testing if
    they are correctly detected.

    This was written to validate that find_one_error() works for all outputs.
    """
    gates = {}
    for line in input_txt.split('\n\n')[1].split('\n'):
        var1, cmd, var2, _, target = line.split(' ')
        var1, var2 = sorted((var1, var2))
        gates[(var1, cmd, var2)] = target
    inv_gates = {val: key for key, val in gates.items()}
    p2 = []
    for _ in range(4):
        var1, var2 = find_one_error(gates)
        p2.extend([var1, var2])
        gates[inv_gates[var1]], gates[inv_gates[var2]] = var2, var1
        inv_gates = {val: key for key, val in gates.items()}
    p2 = ','.join(sorted(p2))
    print(p2 == AOC_ANSWER[1], p2)
    ans = find_one_error(gates)
    assert ans == None
    print('Fixed input')
    correct_gates = gates.copy()
    # codes, inv_codes = {}, {}
    codes['a00'] = gates[('x00', 'AND', 'y00')]
    codes['z00'] = gates[('x00', 'XOR', 'y00')]
    for idx in range(1, 45):
        previous_a = f'a{idx-1:02}'
        a, b, c, d, x, y, z = (f'{axis}{idx:02}' for axis in 'abcdxyz')
        codes[b] = gates[(x, 'XOR', y)]
        codes[c] = gates[(x, 'AND', y)]
        codes[d] = gates[gkey(codes[previous_a], codes[b], 'AND')]
        codes[z] = gates[gkey(codes[previous_a], codes[b], 'XOR')]
        codes[a] = gates[gkey(codes[c], codes[d], 'OR')]
    for key, val in codes.items():
        inv_codes[val] = key
    for var1, var2 in it.combinations(gates.values(), r=2):
        abc1, abc2 = sorted((inv_codes[var1], inv_codes[var2]))
        print(f'Force swapping {var1} ({inv_codes[var1]}) WITH {var2} ({inv_codes[var2]})')
        if abc1[0] == 'a' and abc2[0] == 'b':
            if int(abc1[1:]) + 1 == int(abc2[1:]):
                print('This error does not lead to change in z')
                continue
        if abc1[0] == 'c' and abc2[0] == 'd':
            if abc1[1:] == abc2[1:]:
                print('This error does not lead to change in z')
                continue
        key1 = inv_gates[var1]
        key2 = inv_gates[var2]
        gates = correct_gates.copy()
        gates[key1], gates[key2] = gates[key2], gates[key1]
        ans = find_one_error(gates)
        assert {var1, var2} == {*ans}, f'{var1}, {var2} ≠ {ans}'
        if ans == None:
            raise(Exception('No solution found...'))

@print_function
def main(input_txt: str) -> tuple[int, int]:
    return (
        part_one(input_txt),
        part_two(input_txt)
    )

aoc_run( __name__, __file__, main, AOC_ANSWER)
