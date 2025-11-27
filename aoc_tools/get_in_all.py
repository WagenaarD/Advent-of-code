"""
Gets all input files
"""

__project__   = 'Advent-of-code'
__author__    = 'DW'
__copyright__ = ''
__version__   = '1.0.1'

from get_aoc_in import get_aoc_in, COOKIE, COOKIE_PATH, COOKIE_PLACEHOLDER, SCRIPT_PATH
import os
import re

def get_all_in() -> None:
    """
    Gets input files for all days of all years based on folder names. Usefull for when cloning the 
    repository without input files
    """
    if COOKIE == COOKIE_PLACEHOLDER:
        print(f'Cookie is still set at template, update {COOKIE_PATH} first')
        return
    for year in sorted(os.listdir(SCRIPT_PATH.parent)):
        year_path = SCRIPT_PATH.parent / year
        if year_path.is_dir and re.fullmatch('\\d{4}', year):
            print(year_path)
            for day in sorted(os.listdir(year_path)):
                day_path = year_path / day
                if day_path.is_dir and re.fullmatch('day_\\d{2}', day):
                    if 'in' not in os.listdir(day_path):
                        print('', day_path)
                        get_aoc_in(day_path)
            

    
    


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    get_all_in()