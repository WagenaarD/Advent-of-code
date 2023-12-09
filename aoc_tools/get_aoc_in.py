"""
Move to the directory of the appropriate day and run with the following command:
python3 ../_utils/get_aoc_in.py

Will retreive the input file

Requires the presence of a file in the _utils folder named aoc_session_cookie.json containing the 
cookie variable for the session cookie. Update this cookie when the script no longer works. The 
cookie should last about a month, so updating at the end of each november should be enough.

Original idea was based on a bash script:
 - https://www.reddit.com/r/adventofcode/comments/e32v5b/need_help_with_input_download_script_bash/
 - https://github.com/Janiczek/advent-of-code/blob/master/start.sh#L8-L11
"""

__project__   = 'get_advent_of_code_input_file'
__author__    = 'dirk.wagenaar@gmail.com'
__copyright__ = 'not really'
__version__   = '1.0.2'

import json
import requests
import os

# Get cookie
script_path = '/'.join(__file__.replace('\\', '/').split('/')[:-1])
with open(script_path + '/aoc_session_cookie.json') as f:
    cookie = json.loads(f.read())['cookie']  

# Get the day parameters based on the current folder
year, day_folder = os.getcwd().replace('\\', '/').split('/')[-2:]
day = day_folder[-2:]
day_no_zero = str(int(day))

# Retreive the response
response = requests.get(
    url=f'https://adventofcode.com/{year}/day/{day_no_zero}/input', 
    cookies={'session': cookie}, 
    headers={}
)

# Remove trailing linebreak
content = response.content.decode()
if content.endswith('\n'):
    content = content [:-1]

# Write the output
print(content)
with open('in', 'w') as f:
    f.write(content)
