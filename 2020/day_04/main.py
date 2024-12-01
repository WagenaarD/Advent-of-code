"""
Advent of code challenge
python3 ../../aoc_tools/get_aoc_in.py
python3 main.py < in
"""

AOC_ANSWER = (247, 145)

import sys
from pathlib import Path
sys.path.append(str(AOC_BASE_PATH := Path(__file__).parents[2]))
from aoc_tools import print_function, aoc_run
import re

KEYS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

@print_function
def main(input: str) -> int:
    passports = input.split('\n\n')
    p1, p2 = 0, 0
    for pp in passports:
        pp_dict = {}
        for pair in pp.split():
            key, val = pair.split(':')
            pp_dict[key] = val
        if not all(key in pp_dict for key in KEYS):
            continue
        p1 += 1
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if not re.fullmatch('\\d{4}', pp_dict['byr']): continue
        if int(pp_dict['byr']) < 1920 or int(pp_dict['byr']) > 2002: continue
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if not re.fullmatch('\\d{4}', pp_dict['iyr']): continue
        if int(pp_dict['iyr']) < 2010 or int(pp_dict['iyr']) > 2020: continue
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if not re.fullmatch('\\d{4}', pp_dict['eyr']): continue
        if int(pp_dict['eyr']) < 2020 or int(pp_dict['eyr']) > 2030: continue
        # hgt (Height) - a number followed by either cm or in:
        if not re.fullmatch('\\d+(in|cm)', pp_dict['hgt']): continue
        # If cm, the number must be at least 150 and at most 193.
        if pp_dict['hgt'].endswith('cm'):
            height = int(re.findall('\\d+', pp_dict['hgt'])[0])
            if height < 150 or height > 193: continue
        # If in, the number must be at least 59 and at most 76.
        elif pp_dict['hgt'].endswith('in'):
            height = int(re.findall('\\d+', pp_dict['hgt'])[0])
            if height < 59 or height > 76: continue
        else:
            continue
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if not re.fullmatch('#[\\da-f]{6}', pp_dict['hcl']): continue
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        if not pp_dict['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']: continue
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        if not re.fullmatch('\\d{9}', pp_dict['pid']): continue
        # cid (Country ID) - ignored, missing or not.
        p2 += 1
    return p1, p2

aoc_run(__name__, __file__, main, AOC_ANSWER, 'in')


