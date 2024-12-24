"""
Advent of code challenge
To run code, copy to terminal (MacOS):
python3 main.py < in
"""
# 09:51:36
# 10:03:25
# 14:08:01

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import itertools as it
import re

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

def find_error(gates: dict[tuple, str]) -> tuple[tuple, tuple]:
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
    y01      x01                 a01 (carried in)
     │        │  ┌────────────────┤
     │        └───────┬───┐      XOR ─── z01
     │           │    │  XOR ─┬───┘ 
     └──────────────┬─────┘   │  (↑b01)
                 │  │ └───┐   │  (↓c01)
                 │  │    AND ──────┐
                 │  └─────┘   │    OR ── a02 (carried out)
                 │           AND───┘
                 └────────────┘  (↑d01)
    
    We can simulate the logic circuit to find where the layout is erroneous. For my input it was 
    enough to keep a set of A and B variable names (these are used as input for AND and XOR gates) 
    and C and D variables (used as input for OR gates). We can determine the variabele names of A, 
    B, C and D for increasing bits and verify that these 
    
    """
    # Define some helper variables
    inv_gates = {val: key for key, val in gates.items()}
    ABs = set()
    CDs = set()
    for k1, cmd, k2 in gates:
        if cmd in ('AND', 'XOR'):
            ABs.update({k1, k2})
        if cmd == 'OR':
            CDs.update({k1, k2})
    # Check a special case, z00 is determined using only x00 and y00
    key = gkey('x00', 'y00', 'XOR')
    if gates[key] != 'z00':
        print('    gates[key] != \'z00\'')
        return (key, inv_gates['z00'])
    # All other cases should have 4 operations
    varA_key = gkey('x00', 'y00', 'AND')
    assert varA_key in gates, f'gates[{varA_key}] does not exist. This should be impossible'
    varA = gates[varA_key]
    for idx in range(1, 45):
        varX, varY, varZ = (f'{axis}{idx:02}' for axis in 'xyz')
        varB, varC, varD = '', '', ''
        varB = gates[gkey(varX, varY, 'XOR')]
        # Both A and B should be part of the set ABs. If not, the 
        if varA not in ABs:
            # B should share an AND and a XOR gate with A
            swap1_key = inv_gates[varA]
            for k1, cmd, k2 in gates:
                if cmd in ('AND', 'XOR') and varB in (k1, k2):
                    swap2_out = k2 if k1 == varB else k1
                    swap2_key = inv_gates[swap2_out]
                    break   
            print('    varA not in ABs')
            return (swap1_key, swap2_key)
        if varB not in ABs:
            # B should share an AND and a XOR gate with A
            swap1_key = inv_gates[varB]
            for (k1, cmd, k2), out in gates.items():
                if cmd in ('AND', 'XOR') and varA in (k1, k2):
                    swap2_out = k2 if k1 == varA else k1
                    swap2_key = inv_gates[swap2_out]
                    break      
            print('    varB not in ABs')          
            return (swap1_key, swap2_key)
        varZ_key = gkey(varA, varB, 'XOR')
        varD_key = gkey(varA, varB, 'AND')
        if varZ_key not in gates or varD_key not in gates:
            # (Did not happen for my input)
            k1, cmd, k2 = inv_gates[varZ]
            if varA == max([varA, varB, k1, k2], key=len):
                swap1_key = inv_gates[varB]
                swap2_key = inv_gates[k1 if k2 == varA else varB]
            else:
                swap1_key = inv_gates[varA]
                swap2_key = inv_gates[k1 if k2 == varB else varA]
            print('    varZ_key not in gates or varD_key not in gates')
            return (swap1_key, swap2_key)
        if gates[varZ_key] != varZ:
            # varA XOR varB should be equal to varZ
            swap1_key = varZ_key
            swap2_key = inv_gates[varZ]
            print('    gates[varZ_key] != varZ')
            return (swap1_key, swap2_key)
        varC = gates[gkey(varX, varY, 'AND')]
        varD = gates[varD_key]
        if varC not in CDs:
            # C should share an OR gate with D
            swap1_key = inv_gates[varC]
            for (k1, cmd, k2), out in gates.items():
                if cmd == 'OR' and varD in (k1, k2):
                    swap2_out = k2 if k1 == varD else k1
                    swap2_key = inv_gates[swap2_out]
                    break
            print('    varC not in CDs')
            return (swap1_key, swap2_key)
        if varD not in CDs:
            # C should share an OR gate with D
            swap1_key = inv_gates[varD]
            for (k1, cmd, k2), out in gates.items():
                if cmd == 'OR' and varC in (k1, k2):
                    swap2_out = k2 if k1 == varC else k1
                    swap2_key = inv_gates[swap2_out]
                    break
            print('    varD not in CDs')
            return (swap1_key, swap2_key)
        varA_key = gkey(varC, varD, 'OR')
        if varA_key not in gates:
            # C XOR D does not exist, so either C or D is wrong (did not happen for my input)
            print('    varA_key not in gates')
            for k1, cmd, k2 in gates:
                if cmd == 'OR':
                    if varC in (k1, k2):
                        swap1_key = inv_gates[varD]
                        swap2_key = inv_gates[k1 if varC == k2 else k1]
                        return swap1_key, swap2_key
                    elif varD in (k1, k2):
                        swap1_key = inv_gates[varC]
                        swap2_key = inv_gates[k1 if varD == k2 else k1]
                        return swap1_key, swap2_key
        varA = gates[varA_key]
        if idx == 44:
            if varA != 'z45':
                assert False, f'a45 != z45 is not implemented'
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
        gates[gkey(key1, key2, cmd)] = target
    swapped_outputs = []
    for idx in range(6):
        ans = find_error(gates)
        if ans == None:
            break
        key1, key2 = ans
        print(f'Swap proposed:')
        print(f'  gates[{key1}] ≠ {gates[key1]}')
        print(f'  gates[{key2}] ≠ {gates[key2]}')
        swapped_outputs.extend([gates[key1], gates[key2]])
        gates[key1], gates[key2] = gates[key2], gates[key1]
    else:
        raise(Exception(f'Reached maximum number of fixes after {idx+1} iterations'))
    return ','.join(map(str, sorted(swapped_outputs)))
    
def test(input_txt):
    """
    Our input did not contain all types of swaps, so in this function we test if our code can detect
    all types of swaps by first fixing the code and then adding all possible swaps and testing if 
    they are correctly detected.
    """
    gates = {}
    for line in input_txt.split('\n\n')[1].split('\n'):
        key1, cmd, key2, _, target = line.split(' ')
        gates[gkey(key1, key2, cmd)] = target
    for _ in range(4):
        key1, key2 = find_error(gates)
        gates[key1], gates[key2] = gates[key2], gates[key1]
    ans = find_error(gates)
    assert ans == None
    print('Fixed input')
    correct_gates = gates.copy()
    coded_keys = {}
    coded_keys['a00'] = gkey('x00', 'y00', 'AND')
    assert coded_keys['a00'] in correct_gates, f'{coded_keys['a00']}'
    for idx in range(1, 45):
        previous_a = f'a{idx-1:02}'
        previous_a_val = correct_gates[coded_keys[previous_a]]
        a, b, c, d, x, y, z = (f'{axis}{idx:02}' for axis in 'abcdxyz')
        coded_keys[b] = gkey(x, y, 'XOR')
        coded_keys[c] = gkey(x, y, 'AND')
        assert coded_keys[b] in correct_gates, f'{coded_keys[b]}'
        assert coded_keys[c] in correct_gates, f'{coded_keys[c]}'
        b_val = correct_gates[coded_keys[b]]
        c_val = correct_gates[coded_keys[c]]
        coded_keys[d] = gkey(previous_a_val, b_val, 'AND')
        d_val = correct_gates[coded_keys[d]]
        coded_keys[a] = gkey(c_val, d_val, 'OR')
        assert coded_keys[d] in correct_gates, f'{coded_keys[d]}'
        assert coded_keys[a] in correct_gates, f'{coded_keys[a]}'
    inv_codes = {correct_gates[val]: key for key, val in coded_keys.items()}
    
    for key1, key2 in it.combinations(gates, r=2):
        print(f'Swapping \n - gates[{key1}]: {gates[key1]} (={inv_codes[gates[key1]]}) WITH \n - gates[{key2}]: {gates[key2]} (={inv_codes[gates[key2]]})')
        # print(f'  {gates[key1]} (={inv_codes[gates[key1]]}) WITH {gates[key2]} (={inv_codes[gates[key2]]})')
        gates = correct_gates.copy()
        gates[key1], gates[key2] = gates[key2], gates[key1]
        ans = find_error(gates)
        print(ans)
        assert {key1, key2} == {*ans}, f'{key1}, {key2} ≠ {ans}'
        if ans == None:
            raise(Exception('BLEGH'))


@print_function
def main(input_txt: str) -> tuple[int, int]:
    # return test(input_txt)
    return (
        part_one(input_txt), 
        part_two(input_txt)
    )
aoc_run(__name__, __file__, main, AOC_ANSWER)


