# -*- coding: utf-8 -*-

#    QMaton is a Python/Qt software used to run cellular automatons.
#    Copyright (C) 2021  Rémi Ducceschi (remileduc) <remi.ducceschi@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Neighborhood utils."""


from functools import wraps


def rule_margin(radius=1):
    """Rule decorator to check if grid[x][y] is out of the radius margin.

    if it is, it returns grid[x][y], otherwise it returns the call.
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
