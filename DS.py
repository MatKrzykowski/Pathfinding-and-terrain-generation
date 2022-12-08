# DS.py

# Libraries import
import numpy as np

from point import Point

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


def map_graph(hmap, endpoint, is_distancemap=False):
    """Print 2D map function using matplotlib with visible path between endpoints.

    hmap - imported heightmap
    endpoint - member of point class containing path between endpoints
    is_distancemap - is distance or height map to be printed

    A - printed 2D array
    """

    # Matplotlib libraries import
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches

    n = len(hmap)  # Compute sidelength of the map

    # Copy distancemap to A
    if is_distancemap:
        A = np.array([[hmap[i][j].d for i in range(n)] for j in range(n)])
    # Copy height map to A
    else:
        A = np.array([[hmap[i][j].h for i in range(n)] for j in range(n)])

    # Copy path assigned to end point
    verts = endpoint.path
    # Assign codes to the verts
    codes = [Path.LINETO for i in range(len(verts))]  # optional Path.CURVE4
    codes[0] = Path.MOVETO  # Start point code

    # Preparing path to be printed
    path = Path(verts, codes)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, edgecolor='red', facecolor='none', lw=1)
    ax.add_patch(patch)

    # Preparing map to be printed
    plt.imshow(A, cmap='bone', interpolation='nearest')

    # Printing the result
    plt.show()


def graph_3d(hmap):
    """3d visualization of the heightmap.

    hmap - imported heightmap"""

    # Libraries import
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    n = len(hmap)  # Compute sidelength of the map

    # Prepare data for the plot
    I = np.array([i for i in range(n)])
    X, Y = np.meshgrid(I, I)
    Z = np.array([[hmap[i][j].h for i in range(n)] for j in range(n)])

    # Prepare plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, color='r')
    surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5,
                           cmap=plt.cm.coolwarm, linewidth=0)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()  # Print 3d map


def hmap_gen(m, scale_factor, exp_factor):
    """Height map generator using diamond-square algorith. Returns heightmap with generated points.

    m - number of diamond-square algorithm steps, determines sidelength of the map to be 2**m + 1,
    scale_factor - determines range of heights,
    exp_factor - determines the smootheness of the heightmap.
    """

    n = 2**m + 1  # Sidelength of the heightmap

    # Generate n by n matrix of point objects
    hmap = [[Point(0.0, i, j, path=[]) for j in range(n)] for i in range(n)]

    # Corner points generator to start off DSA
    hmap[0][0].h = np.random.randn() * scale_factor
    hmap[2**m][0].h = np.random.randn() * scale_factor
    hmap[0][2**m].h = np.random.randn() * scale_factor
    hmap[2**m][2**m].h = np.random.randn() * scale_factor
    # Center assigned for "hill" feature
    hmap[2**(m - 1)][2**(m - 1)].h = 3 * scale_factor

    # Loop over m - number of stages of the algorithm
    for i in range(m):
        x = 2**(m - i - 1)  # Variable assigned to speed up computation

        # Squere centers
        factor = scale_factor * exp_factor**(-i - 1)  # Modified scale factor
        for j in range(2**i):  # Loop over x axis
            for k in range(2**i):  # Loop over y axis
                jx2 = j * x * 2  # Variable assigned to speed up computation
                kx2 = k * x * 2  # Variable assigned to speed up computation

                target = hmap[jx2 + x][kx2 + x]  # Get object from the matrix
                if target.h == 0:  # Skip if point already evaluated
                    # Add values of the neighbors
                    target.h = hmap[jx2][kx2].h + hmap[jx2 + 2 * x][kx2].h +\
                        hmap[jx2][kx2 + 2 * x].h + \
                        hmap[jx2 + 2 * x][kx2 + 2 * x].h
                    target.h = target.h / 4  # Divide to get average
                    target.h += np.random.randn() * factor  # Add random value

        # Diamond centers
        y = 2**(i + 1)  # Variable assigned to speed up computation
        factor = scale_factor * exp_factor**(-i - 1.5)  # Modified scale factor
        for j in range(y + 1):  # Loop over x axis
            for k in range(y + 1):  # Loop over y axis
                l = 0  # Number of added values used to calculate average
                jx = j * x  # Variable assigned to speed up computation
                kx = k * x  # Variable assigned to speed up computation
                target = hmap[jx][kx]  # Get object from the matrix
                if target.h == 0:  # Was point already evaluated
                    if j != 0:  # Left border check
                        target.h += hmap[jx - x][kx].h
                        l += 1
                    if j != (y):  # Right border check
                        target.h += hmap[jx + x][kx].h
                        l += 1
                    if k != 0:  # Upper border check
                        target.h += hmap[jx][kx - x].h
                        l += 1
                    if k != (y):  # Lower corner check
                        target.h += hmap[jx][kx + x].h
                        l += 1
                    # Divide to get average
                    target.h = target.h / l
                    target.h += np.random.randn() * factor  # Add random value
    return hmap


def path_step(origin, x, y, z, unvisited, hmap, n):
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
            a = origin.d + origin.dist(go_to, z)
            # If shorter than previous one
            if a < go_to.d:
                go_to.d = a  # Assign shorter path length
                # Assign new path appended by go_to point's position
                go_to.path = origin.path + [go_to.pos]
                # Add to unvisited set (if wasn't there already)
                unvisited.add(go_to)

#####################################################################


def dijkstra(m=8, random_endpoints=False):
    """Function performing Dijkstra's algorithm on the generated heightmap.

    m - number of stages of diamond-square algorithm
    random_endpoints - Boolean deciding whether or not endpoints should be assigned
    at random or should be put in the opposite corners."""

    # Parameters
    n = 2**m + 1  # Sidelength of the heightmap
    scale_factor = n / 4  # Height scale factor
    # Scale decresing factor for DSA, the larger the value the smoother the
    # heightmap
    exp_factor = 1.6

    iteration = 0  # Number of Dijkstra's algorithm iterations for logging

    # Height map definition as n by n array of point objects
    hmap = hmap_gen(m, scale_factor, exp_factor)

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
    while True:
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
        x, y = target.pos  # Acquiring target position to evaluate neighbors

        # Performing steps of Dijkstra's algorithm for neighboring points
        path_step(target, x - 1, y, 1, unvisited, hmap, n)
        path_step(target, x + 1, y, 1, unvisited, hmap, n)
        path_step(target, x, y - 1, 1, unvisited, hmap, n)
        path_step(target, x, y + 1, 1, unvisited, hmap, n)
        path_step(target, x - 1, y - 1, 2, unvisited, hmap, n)
        path_step(target, x - 1, y + 1, 2, unvisited, hmap, n)
        path_step(target, x + 1, y - 1, 2, unvisited, hmap, n)
        path_step(target, x + 1, y + 1, 2, unvisited, hmap, n)

        # Logging procedure
        iteration += 1  # Increment of iteration counter
        if iteration % 5000 == 0:  # Print every arbitrary number of iterations
            # Print progress
            print(str(100 * iteration / n**2)[0:4] + "%")

        # Check if target point is in unvisited set
        try:
            del target.path  # Delete its path to free memory
            unvisited.remove(target)  # Remove from unvisited set
            target.visited = True  # Set as visited
        # If not exit the loop
        except AttributeError:
            break  # End the loop

    return hmap, endpoint  # Return for plotting


if __name__ == "__main__":
    hmap, endpoint = dijkstra()

    # Print the results
    map_graph(hmap, endpoint)
    # graph_3d(hmap)
