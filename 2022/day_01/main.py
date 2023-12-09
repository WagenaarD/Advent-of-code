"""
Advent of code challenge 2022
"""

__project__   = 'Advent of code 2022'
__author__    = 'D W'


if __name__ == '__main__':
    """Executed if file is executed but not if file is imported."""
    
    # Part 1
    # Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    # One liner:
    #  - print('Max_calories_per_elf = {}'.format(max([sum([int(cal) for cal in elf_string.split('\n')]) for elf_string in open('input.txt').read().split('\n\n')])))
    full_text = open('input.txt').read()
    summed_calories_per_elf = [sum([int(cal) for cal in elf_string.split('\n')]) \
        for elf_string in full_text.split('\n\n')]
    max_calories_per_elf = max(summed_calories_per_elf)
    print('Max_calories_per_elf = {}'.format(max_calories_per_elf))

    # Part 2
    # Find the top three Elves carrying the most Calories. How many Calories are those Elves 
    # carrying in total?
    summed_calories_per_elf.sort()
    top_three_calories_summed = sum(summed_calories_per_elf[-3:])
    print('Total calories of top three = {}'.format(top_three_calories_summed))
