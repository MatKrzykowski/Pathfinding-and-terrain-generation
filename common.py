from itertools import product
from operator import or_

def neighbors():
    return filter(lambda x: or_(*x), product((-1, 0, 1), repeat=2))