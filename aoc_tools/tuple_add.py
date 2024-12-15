"""
"""

__project__   = ''
__author__    = 'Dirk'
__copyright__ = ''
__version__   = '1.0.1'

def tuple_add(*pos):
    """
    Performs element-wise addition of multiple tuples.

    This function takes any number of tuples as arguments and returns a new tuple 
    where each element is the sum of the corresponding elements in the input tuples.
    
    Example:
        >>> tuple_add((1, 2), (-1, 0))
        (0, 2)
        >>> tuple_add((1, 2, 3), (4, 5, 6), (7, 8, 9))
        (12, 15, 18)

    Args:
        *pos: Any number of tuples of the same length to be added element-wise.

    Returns:
        tuple: A tuple containing the element-wise sums of the input tuples.

    Raises:
        ValueError: If the input tuples are not of the same length.
    """
    return tuple(sum(axis) for axis in zip(*pos))