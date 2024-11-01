from functools import reduce
from operator import iconcat


def flatten(x):
    return reduce(iconcat, x, [])
