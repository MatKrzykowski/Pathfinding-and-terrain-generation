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


def path_step(origin, goal, path, d, to_be_visited,):
    """Function performing single step of Dijkstra's algorithm.

    origin - origin point,
    x,y - go-to point,
    z - distance in x-y plane, 1 for direct and 2 for diagonal neighbors,
    to_be_visited - set of to_be_visited points
    hmap - heightmap
    n - sidelength of the heightmap."""

    heapq.heappush(
        to_be_visited,
        [d + origin.dist(goal), path + [goal.pos]]
    )


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
    to_be_visited = [[startpoint.d, [startpoint.pos]]]

    visited = np.zeros((n, n), "bool")

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
            if not visited[x, y]:
                origin = hmap[x][y]
                visited[x, y] = True
                break

        if x == x2 and y == y2:
            return path + [endpoint.pos]

        for dx, dy in neighbors():
            if 0 <= x + dx < n and 0 <= y + dy < n:
                goal = hmap[x + dx][y + dy]
                path_step(origin, goal, path, d, to_be_visited)
