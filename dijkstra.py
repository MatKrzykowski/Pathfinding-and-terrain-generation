"""dijkstra.py"""

import numpy as np
from tqdm import tqdm
from common import neighbors


def gen_points(n):
    """Random endpoints coordinates generator function

    Returns tuple of two points (x, y) which distance is guaranteed to be larger
    than side of the map.
    n - sidelenght of the map"""

    while True:  # Execute until rights points are found
        # Random integers from 0 to n-1
        x1, y1, x2, y2 = np.random.randint(n, size=4)

        # Exit if distance between points larger than side length
        if (x1 - x2)**2 + (y1 - y2)**2 > n**2:
            return (x1, y1, x2, y2)


def path_step(origin, x, y, unvisited, hmap, n):
    """Function performing single step of Dijkstra's algorithm.

    origin - origin point,
    x,y - go-to point,
    z - distance in x-y plane, 1 for direct and 2 for diagonal neighbors,
    unvisited - set of unvisited points
    hmap - heightmap
    n - sidelength of the heightmap."""

    # Check if origin point is not on the boundary
    if min(x, y) != -1 and max(x, y) != n:
        # Check if go-to point was already visited
        go_to = hmap[x][y]
        if not go_to.visited:
            # Calculating new path length to go-to point
            a = origin.d + origin.dist(go_to)
            # If shorter than previous one
            if a < go_to.d:
                go_to.d = a  # Assign shorter path length
                # Assign new path appended by go_to point's position
                go_to.path = origin.path + [go_to.pos]
                # Add to unvisited set (if wasn't there already)
                unvisited.add(go_to)


def dijkstra(hmap, params, random_endpoints=False):
    """Function performing Dijkstra's algorithm on the generated heightmap.

    m - number of stages of diamond-square algorithm
    random_endpoints - Boolean deciding whether or not endpoints should be assigned
    at random or should be put in the opposite corners."""

    n = params.n
    # Path endpoints generation
    if random_endpoints:  # Random
        x1, y1, x2, y2 = gen_points(n)
    else:  # Determined to be in the opposite corners
        x1, y1, x2, y2 = 0, 0, n - 1, n - 1

    # Assigning startpoint
    startpoint = hmap[x1][y1]
    startpoint.d = 0.0  # Setting distance of starting point as 0.0
    startpoint.path = [startpoint.pos]  # Setting path
    unvisited = {startpoint}  # Unvisited set declaration

    # Assigning endpoint
    endpoint = hmap[x2][y2]

    # Infinite loop executing Dijkstra's algorithm
    # Breaks after endpoint is visited
    for _ in tqdm(range(n**2)):
        # Setting current minimal distance as distance of the endpoint
        min_dist = endpoint.d
        target = startpoint  # Temporary assignment

        # Looking for minimal distance among unvisited points
        for p in unvisited:
            # If lesser distance is found
            if min_dist > p.d:
                # Setting new minimal distance
                min_dist = p.d
                target = p
        x, y = target.x, target.y  # Acquiring target position to evaluate neighbors

        # Performing steps of Dijkstra's algorithm for neighboring points
        for i, j in neighbors():
            path_step(target, x + i, y + j, unvisited, hmap, n)

        # Check if target point is in unvisited set
        try:
            del target.path  # Delete its path to free memory
            unvisited.remove(target)  # Remove from unvisited set
            target.visited = True  # Set as visited
        # If not exit the loop
        except AttributeError:
            break  # End the loop

    return endpoint  # Return for plotting