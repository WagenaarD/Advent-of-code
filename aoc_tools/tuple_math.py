"""
"""

__project__   = ''
__author__    = 'Dirk'
__copyright__ = ''
__version__   = '1.0.1'

import operator
from numbers import Number
from typing import Union

Tuple2D = tuple[Number, Number]


def tuple_add(first: Tuple2D, second: Tuple2D) -> Tuple2D:
    """
    Performs element-wise addition of multiple tuples.

    Args:
        *tuples: Any number of tuples with numeric elements to add.

    Returns:
        A tuple where each element is the sum of the corresponding elements in the input tuples.

    Example:
        >>> tuple_add((1, 2), (-1, 0))
        (0, 2)
    """
    return (first[0] + second[0], first[1] + second[1])

def tuple_sub(first: Tuple2D, second: Tuple2D) -> Tuple2D:
    """
    Performs element-wise subtraction of two tuples.

    Args:
        first: The first numeric tuple.
        second: The second numeric tuple.
    
    Example:
        >>> tuple_sub((1, 2), (-1, 0))
        (2, 2)

    Returns:
        A tuple where each element is the result of subtracting the corresponding elements.
    """
    return (first[0] - second[0], first[1] - second[1])

def tuple_mult(first: Tuple2D, second: Union[Tuple2D, Number]) -> Tuple2D:
    """
    Performs element-wise multiplication of a tuple with another tuple or a scalar.

    Args:
        first: A numeric tuple.
        second: A numeric tuple of the same length as `first` or a scalar.
    
    Example:
        >>> tuple_mult((1, 2), (-1, 0))
        (-1, 0)
        >>> tuple_mult((1, 2), 2)
        (2, 4)

    Returns:
        A tuple where each element is the result of the multiplication.
    """
    if isinstance(second, tuple):
        return (first[0] * second[0], first[1] * second[1])
    else:
        return (first[0] * second, first[1] * second)

def tuple_rotate_right(pos: Tuple2D) -> Tuple2D:
    """
    Rotates a 2-D position 90 degrees clockwise around the origin (0, 0).

    Args:
        pos: A 2D numeric tuple (x, y).

    Returns:
        A tuple representing the rotated position.
    """
    return (pos[1], -pos[0])

def tuple_rotate_left(pos: Tuple2D) -> Tuple2D:
    """
    Rotates a 2-D position 90 degrees counterclockwise around the origin (0, 0).

    Args:
        pos: A 2D numeric tuple (x, y).

    Returns:
        A tuple representing the rotated position.
    """
    return (-pos[1], pos[0])


class Pos(tuple):
    """
    A tuple subclass that supports basic element-wise arithmetic operations. Typicaly usefull for 2D
    coordinate or direction representation in grids.
    
    While helpful, Using a Pos is not as fast as using builtin tuples.
    """
    def __new__(cls, iterable):
        """Since tuple is immutable, we override new instead of init"""
        iterable = tuple(iterable)
        assert len(iterable) == 2
        return super(Pos, cls).__new__(cls, tuple(iterable))

    @property
    def manhattan(self) -> int | float:
        """Returns the Manhattan distance (dx + dy) of Pos"""
        return abs(self[0]) + abs(self[1])

    def __repr__(self) -> str:
        """Returns a string representation of the Pos."""
        return f"Pos({', '.join(map(str, self))})"

    def rotate_right(self) -> 'Pos':
        """Rotates a 2-D position 90 degrees right around (0, 0)"""
        return Pos((self[1], -self[0]))
    
    def rotate_left(self) -> 'Pos':
        """Rotates a 2-D position 90 degrees left around (0, 0)"""
        return Pos((-self[1], self[0]))

    def __abs__(self) -> 'Pos':
        """Returns a tuple with the absolute values of each element."""
        return Pos((abs(self[0]), abs(self[1])))

    def __neg__(self) -> 'Pos':
        """Returns a tuple with each element negated."""
        return Pos((-self[0], -self[1]))
    
    def __apply_operator(self, oper, other: tuple | int | float) -> 'Pos':
        """
        Applies either element-wise or scalar 
        """
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError(f"Pos can only process element-wise {oper.__name__} with a 2D tuple-like, not {len(other)=}")
            return Pos((oper(self[0], other[0]), oper(self[1], other[1])))
        elif isinstance(other, int) or isinstance(other, float):
            return Pos((oper(self[0], other), oper(self[1], other)))
        else:
            raise ValueError(f"Pos can only process {oper.__name__} operation with 2D tuple-likes, floats or ints, not {type(other)}")

    def __mul__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) multiplication"""
        return self.__apply_operator(operator.mul, other)

    def __truediv__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) true division"""
        return self.__apply_operator(operator.truediv, other)

    def __add__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) addition"""
        return self.__apply_operator(operator.add, other)

    def __sub__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) subtraction"""
        return self.__apply_operator(operator.sub, other)

    def __floordiv__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) floor division"""
        return self.__apply_operator(operator.floordiv, other)

    def __mod__(self, other: tuple | int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) modulus operation"""
        return self.__apply_operator(operator.mod, other)

    def __pow__(self, other: int | float) -> 'Pos':
        """Performs scalar (int or float) or element-wise (2D tuple) power operation"""
        return self.__apply_operator(operator.pow, other)
    