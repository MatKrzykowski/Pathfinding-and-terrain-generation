"""point.py"""

import numpy as np


class Point:
    """Class describing single point on the heightmap."""

    def __init__(self, z, x, y, path):
        """Initialization method"""
        self.d = np.inf  # distance from the startpoint, set to infinity as per DA
        self.x = x
        self.y = y
        self.z = z
        self.path = path  # path to the point, initialized empty
        self.visited = False  # check if point was visited by DA yet

    @property
    def pos(self):
        """Returns 3D point position as numpy array"""
        return np.array([self.x, self.y, self.z])

    def dist(self, other):
        """Method calculating distance between two others given poth points."""
        return np.linalg.norm(self.pos - other.pos)
