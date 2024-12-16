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

def tuple_mult(pos, factor):
    """
    Performs element-wise multiplication of a tuples and a constant factor
    """
    return tuple(axis*factor for axis in pos)

class Tup(tuple):
    """
    A tuple subclass that supports basic element-wise arithmetic operations. Typicaly usefull for 2D
    coordinate or direction representation in grids.
    """

    def rotate_right(self) -> 'Tup':
        """Rotates a 2-D position 90 degrees right around (0, 0)"""
        assert len(self) == 2
        return Tup((self[1], -self[0]))
    
    def rotate_left(self) -> 'Tup':
        """Rotates a 2-D position 90 degrees left around (0, 0)"""
        assert len(self) == 2
        return Tup((-self[1], self[0]))

    def __abs__(self) -> 'Tup':
        """Returns a tuple with the absolute values of each element."""
        return Tup(map(abs, self))

    def __neg__(self) -> 'Tup':
        """Returns a tuple with each element negated."""
        return Tup(-axis for axis in self)

    def __mul__(self, other) -> 'Tup':
        """
        Performs element-wise multiplication with another tuple
        or scalar multiplication if `other` is not a tuple.
        """
        if isinstance(other, tuple):
            if len(self) != len(other):
                raise ValueError("Tuples must have the same length for element-wise multiplication.")
            return Tup(left * right for left, right in zip(self, other))
        return Tup(axis * other for axis in self)

    def __truediv__(self, other) -> 'Tup':
        """
        Performs element-wise division by a scalar.
        Raises ZeroDivisionError if dividing by zero.
        """
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return Tup(axis / other for axis in self)

    def __add__(self, other: tuple) -> 'Tup':
        """
        Performs element-wise addition with another tuple.
        """
        if len(self) != len(other):
            raise ValueError("Tuples must have the same length for addition.")
        return Tup(left + right for left, right in zip(self, other))

    def __sub__(self, other: tuple) -> 'Tup':
        """
        Performs element-wise subtraction with another tuple.
        """
        if len(self) != len(other):
            raise ValueError("Tuples must have the same length for subtraction.")
        return Tup(left - right for left, right in zip(self, other))

    def __floordiv__(self, other) -> 'Tup':
        """
        Performs element-wise floor division by a scalar.
        Raises ZeroDivisionError if dividing by zero.
        """
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return Tup(axis // other for axis in self)

    def __mod__(self, other) -> 'Tup':
        """
        Performs element-wise modulus operation by a scalar.
        """
        if other == 0:
            raise ZeroDivisionError("Modulus by zero is not allowed.")
        return Tup(axis % other for axis in self)

    def __pow__(self, power: int) -> 'Tup':
        """
        Raises each element of the tuple to the given power.
        """
        return Tup(axis**power for axis in self)

    def __repr__(self) -> str:
        """Returns a string representation of the Tup."""
        return f"Tup({', '.join(map(str, self))})"


    