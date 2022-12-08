# Point.py

from numpy import inf, sqrt


class Point:
    """Class describing single point on the heightmap."""

    def __init__(self, height, x, y, path):
        """Initialization method"""
        self.h = height  # height, generated by DSA
        self.d = inf  # distance from the startpoint, set to infinity as per DA
        self.pos = (x, y)  # position vector
        self.path = path  # path to the point, initialized empty
        self.visited = False  # check if point was visited by DA yet

    def dist(self, neighbor, z):
        """Method calculating distance between two neighbors given poth points.

        z - distance squared in x-y plane"""

        return sqrt(z + (self.h - neighbor.h)**2)
