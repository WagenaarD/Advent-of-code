"""
Move to the directory of the appropriate day and run with the following command:
python3 ../../aoc_tools/get_aoc_in.py

Will retreive the input file

Requires the presence of a file in the _utils folder named aoc_session_cookie.json containing the 
cookie variable for the session cookie. Update this cookie when the script no longer works. The 
cookie should last about a month, so updating at the end of each november should be enough.

Original idea was based on a bash script:
 - https://www.reddit.com/r/adventofcode/comments/e32v5b/need_help_with_input_download_script_bash/
 - https://github.com/Janiczek/advent-of-code/blob/master/start.sh#L8-L11

Example of aoc_session_cookie.json:
""
How to find the cookie
- Open adventofcode.com in Google Chrome
- Login
- Open the Developer tools (Alt, Cmd, I)
- Go to Application, Cookies, https://adventofcode..., session
- Copy the cookie 
"""

__project__   = 'get_advent_of_code_input_file'
__author__    = 'DW'
__copyright__ = ''
__version__   = '1.0.2'

import requests
import os
from pathlib import Path
# import re

# Get cookie
SCRIPT_PATH = Path(__file__).parent
with open(SCRIPT_PATH / 'aoc_session_cookie') as f:
    COOKIE = f.read()
URL = 'https://adventofcode.com/{}/day/{}'

def get_aoc_in(path: Path = None):
    if path == None:
        path = Path(os.getcwd())

    # Get the day parameters based on the current folder
    year = path.parts[-2]
    day_folder = path.parts[-1]
    day = day_folder[-2:]
    day_no_zero = str(int(day))

    # Retreive the response
    response = requests.get(
        url=f'https://adventofcode.com/{year}/day/{day_no_zero}/input', 
        cookies={'session': COOKIE}, 
        headers={}
    )

    # Remove trailing linebreak
    content = response.content.decode()
    if content.endswith('\n'):
        content = content [:-1]

    # Write the output
    print(content)
    print(URL.format(year, day_no_zero))
    with open(path / 'in', 'w') as f:
        f.write(content)

    # # Retreive assignment
    # response = requests.get(
    #     url=f'https://adventofcode.com/{year}/day/{day_no_zero}', 
    #     cookies={'session': COOKIE}, 
    #     headers={}
    # )
    # content = response.text
    # body = re.search('<article[.\n]*', content)

if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    get_aoc_in()