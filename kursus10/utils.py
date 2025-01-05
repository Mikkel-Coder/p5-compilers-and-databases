"""
This file IS NOT IMPORTANT
"""
from functools import reduce
from operator import iconcat


def flatten(x):
    """Removes evert single () {} from x and returns [x] (in a list)
    """
    return reduce(iconcat, x, [])
