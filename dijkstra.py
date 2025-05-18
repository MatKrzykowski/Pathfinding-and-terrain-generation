"""dijkstra.py"""

import heapq

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


def path_step(origin, path, d, x, y, to_be_visited, hmap, n):
    """Function performing single step of Dijkstra's algorithm.

    origin - origin point,
    x,y - go-to point,
    z - distance in x-y plane, 1 for direct and 2 for diagonal neighbors,
    to_be_visited - set of to_be_visited points
    hmap - heightmap
    n - sidelength of the heightmap."""

    # Check if origin point is not on the boundary
    if min(x, y) != -1 and max(x, y) != n:
        # Check if go-to point was already visited
        go_to = hmap[x][y]
        if not go_to.visited:
            # Calculating new path length to go-to point
            d += origin.dist(go_to)
            # If shorter than previous one
            heapq.heappush(to_be_visited, [d, path + [go_to.pos]])


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
    startpoint.d = 0
    to_be_visited = [[startpoint.d, [startpoint.pos]]]  # to_be_visited set declaration

    # Assigning endpoint
    endpoint = hmap[x2][y2]

    # Infinite loop executing Dijkstra's algorithm
    # Breaks after endpoint is visited
    for _ in tqdm(range(n**2)):

        while True:
            d, path = heapq.heappop(to_be_visited)
            x, y, _ = path[-1]
            x = int(x)
            y = int(y)
            point = hmap[x][y]
            if not point.visited:
                break

        if x == x2 and y == y2:
            return path + [endpoint.pos]
        
        
        point.visited = True

        for i, j in neighbors():
            path_step(point, path, d, x + i, y + j, to_be_visited, hmap, n)