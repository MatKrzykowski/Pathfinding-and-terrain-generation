# DS.py

# Libraries import
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path

from dijkstra import dijkstra
from parameters import Params
from point import Point


def map_graph(hmap, path):
    """Print 2D map function using matplotlib with visible path between endpoints.

    hmap - imported heightmap
    endpoint - member of point class containing path between endpoints
    is_distancemap - is distance or height map to be printed

    A - printed 2D array
    """

    n = len(hmap)  # Compute sidelength of the map

    # Copy distancemap to A
    A = np.array([[hmap[i][j].z for i in range(n)] for j in range(n)])

    # Copy path assigned to end point
    verts = np.array(path.get_path())[:, 0:2]
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

    n = len(hmap)  # Compute sidelength of the map

    # Prepare data for the plot
    I = np.arange(n)
    X, Y = np.meshgrid(I, I)
    Z = np.array([[hmap[i][j].z for i in range(n)] for j in range(n)])

    # Prepare plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, color='r')
    surf = ax.plot_surface(
        X, Y, Z, rstride=5, cstride=5, cmap=plt.cm.coolwarm, linewidth=0)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()  # Print 3d map


def hmap_gen(params):
    """Height map generator using diamond-square algorith. Returns heightmap with generated points.

    m - number of diamond-square algorithm steps, determines sidelength of the map to be 2**m + 1,
    scale_factor - determines range of heights,
    exp_factor - determines the smootheness of the heightmap.
    """

    n = 2**m + 1  # Sidelength of the heightmap

    # Generate n by n matrix of point objects
    hmap = [[Point(0.0, i, j) for j in range(n)] for i in range(n)]

    # Corner points generator to start off DSA
    hmap[0][0].z = np.random.randn() * params.scale_factor
    hmap[2**m][0].z = np.random.randn() * params.scale_factor
    hmap[0][2**m].z = np.random.randn() * params.scale_factor
    hmap[2**m][2**m].z = np.random.randn() * params.scale_factor
    # Center assigned for "hill" feature
    hmap[2**(m - 1)][2**(m - 1)].z = 3 * params.scale_factor

    # Loop over m - number of stages of the algorithm
    for i in range(m):
        x = 2**(m - i - 1)  # Variable assigned to speed up computation

        # Squere centers
        factor = params.scale_factor * params.exp_factor**(
            -i - 1)  # Modified scale factor
        for j in range(2**i):  # Loop over x axis
            for k in range(2**i):  # Loop over y axis
                jx2 = j * x * 2  # Variable assigned to speed up computation
                kx2 = k * x * 2  # Variable assigned to speed up computation

                target = hmap[jx2 + x][kx2 + x]  # Get object from the matrix
                if target.z == 0:  # Skip if point already evaluated
                    # Add values of the neighbors
                    target.z = hmap[jx2][kx2].z + hmap[jx2 + 2 * x][kx2].z +\
                        hmap[jx2][kx2 + 2 * x].z + \
                        hmap[jx2 + 2 * x][kx2 + 2 * x].z
                    target.z = target.z / 4  # Divide to get average
                    target.z += np.random.randn() * factor  # Add random value

        # Diamond centers
        y = 2**(i + 1)  # Variable assigned to speed up computation
        factor = params.scale_factor * params.exp_factor**(
            -i - 1.5)  # Modified scale factor
        for j in range(y + 1):  # Loop over x axis
            for k in range(y + 1):  # Loop over y axis
                l = 0  # Number of added values used to calculate average
                jx = j * x  # Variable assigned to speed up computation
                kx = k * x  # Variable assigned to speed up computation
                target = hmap[jx][kx]  # Get object from the matrix
                if target.z == 0:  # Was point already evaluated
                    if j != 0:  # Left border check
                        target.z += hmap[jx - x][kx].z
                        l += 1
                    if j != (y):  # Right border check
                        target.z += hmap[jx + x][kx].z
                        l += 1
                    if k != 0:  # Upper border check
                        target.z += hmap[jx][kx - x].z
                        l += 1
                    if k != (y):  # Lower corner check
                        target.z += hmap[jx][kx + x].z
                        l += 1
                    # Divide to get average
                    target.z = target.z / l
                    target.z += np.random.randn() * factor  # Add random value
    return hmap


if __name__ == "__main__":
    # Parameters
    params = Params(
        m := 10,
        n := 2**m + 1,  # Sidelength of the heightmap
        scale_factor=n,  # Height scale factor
        # Scale decresing factor for DSA, the larger the value the smoother the
        # heightmap
        exp_factor=1.6)

    # Height map definition as n by n array of point objects
    hmap = hmap_gen(params)

    path = dijkstra(hmap, params)

    # Print the results
    map_graph(hmap, path)
    # graph_3d(hmap)
