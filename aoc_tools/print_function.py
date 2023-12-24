"""
Decorator for quickly printing function results
"""

__project__   = ''
__author__    = 'Dirk'
__copyright__ = ''
__version__   = '1.0.1'

import datetime
import inspect


def arg_repr(argument):
    """
    Shortens the arguments and returns a repr string.
    """
    if type(argument) == list:
        if len(argument) > 4:
            return '[{}, ...]'.format(', '.join([repr(item) for item in argument[0:4]]))
        else:
            return repr(argument)
    else:
        return '{:.50}'.format(repr(argument))


def print_function(func = None, start = False, run_time = True, include_args = False, is_method = False, prefix = ''):
    """
    To be used as a decorator: e.g.
        @print_function(prefix = ' - ')
        def function(): ...

    Prints the function call arguments, results and run_time (optional). is_method needs to be set
    to True for methods for correct logging result. Setting start to True also prints the function
    call before running the function which can be usefull for slow functions. Setting a prefix can
    help distinguish these console outputs from other print statements.

    Can also be called directly if no custom arguments are set:
        @print_function
        def function(): ...
    """
    def outer_decorator(function):
        def inner_decorator(*args, **kwargs):
            if is_method:
                output = '{prefix}{parent}.{function}'.format(
                    prefix = prefix,
                    parent = args[0],
                    function = function.__name__,
                )
                fun_args = args[1:]
            else:
                output = '{prefix}{function}'.format(
                    prefix = prefix,
                    function = function.__name__,
                )
                fun_args = args
            if include_args:
                output += '({arguments})'.format(arguments = ', '.join( \
                    [arg_repr(val) for val in fun_args] + \
                    ['{} = {}'.format(key, arg_repr(value)) for key, value in kwargs.items()]
                ))
            else:
                output += '(...)'
            if start:
                print(output)
            start_time = datetime.datetime.now()
            value = function(*args, **kwargs)
            passed = datetime.datetime.now() - start_time
            seconds_passed = passed.days * 24 * 60 * 60 + passed.seconds + passed.microseconds / 1E6
            output += ' = {result}{time}'.format(
                result = arg_repr(value),
                time = ' ({} s)'.format(seconds_passed) if run_time else '',
            )
            print(output)

            return value
        return inner_decorator
    if inspect.isfunction(func):
        return outer_decorator(func)
    return outer_decorator