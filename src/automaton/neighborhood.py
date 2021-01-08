""""Neighborhood"""

from functools import wraps


def rule_margin(radius=1):
    """
    Rule decorator to check that grid[x][y] is out of the radius margin.
    """
    def inner_decorator(rule):

        @wraps(rule)
        def wrapped(grid, x, y):
            # check that grid[x][y] is not in the radius margin
            if x < radius or y < radius or (x + radius) >= len(grid) or (y + radius) >= len(grid[x]):
                return grid[x][y]
            return rule(grid, x, y)

        return wrapped

    return inner_decorator


def count_neighbors(grid, x, y, state, radius=1):
    """
    Count the neighbors of the cell grid[x][y] which have the state `state`.

    `grid[x][y]` is not counted in the result.
    """

    cpt = 0
    for i in range(x - radius, x + radius + 1):
        for j in range(y - radius, y + radius + 1):
            if (i != x or j != y) and grid[i][j] == state:
                cpt += 1
    return cpt


def create_neighborhood(grid, x, y, radius=1):
    """
    Create the neighborhood of the cell grid[x][y]

    Note that the cell grid[x][y] is part of the result in the center:

        result[(radius*2+1) // 2][(radius*2+1) // 2]

    """

    neighborhood = []
    for i in range(x - radius, x + radius + 1):
        neighborhood.append(grid[i][y - radius:y + radius + 1])
    return neighborhood
