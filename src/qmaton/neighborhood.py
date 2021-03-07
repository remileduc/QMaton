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

"""
Neighborhood module.

Utils functions and class to deal with neighborhood of a cell.

.. note:: This file is highly inspired from Richard Feistenauer implementation of the neighborhood in its cellular
          automaton.
          See https://gitlab.com/DamKoVosh/cellular_automaton/-/blob/master/cellular_automaton/neighborhood.py
"""

import enum
import itertools
import math
import operator


class EdgeRule(enum.Enum):
    """ Enum for different possibilities to handle the edge of the automaton. """

    IGNORE_EDGE_CELLS = 0
    """Cells on the edge are ignored and will never change."""
    IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS = 1
    """Cells on the edge are taken in account beut only have partial neighborhood."""
    FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS = 2
    """Cells on the edge act as if they were connected to the other side of the grid."""


class Neighborhood:
    """
    Calculate the neighborhood of a cell.

    The number of cells in the neighborhood of a cell depends on the radius and the edge rule.
    """

    def __init__(self, edge_rule=EdgeRule.IGNORE_EDGE_CELLS, radius=1):
        """General class for all Neighborhoods.
        :param edge_rule:   Rule to define, how cells on the edge of the grid will be handled.
        :param radius:      If radius > 1 it grows the neighborhood
                            by adding the neighbors of the neighbors radius times.
        """
        self._rel_neighbors = None
        self._grid_size = ()
        self._radius = radius
        self.__edge_rule = edge_rule

    def is_on_edge(self, coordinate, grid_size):
        return any(not (self._radius - 1 < ci < di - self._radius) for ci, di in zip(coordinate, grid_size))

    def get_neighbors_coordinates(self, coordinate, grid_size):
        """Get a list of absolute coordinates for the cell neighbors.

        The EdgeRule can reduce the returned neighbor count.
        :param tuple coordinate:  The coordinate of the cell (x, y).
        :param tuple grid_size:  The dimensions of the grid, used for the edges (width, length).
        :return: list of absolute coordinates for the cells neighbors.
        """
        self.__lazy_initialize_relative_neighborhood(grid_size)
        return self.__neighbors_generator(coordinate)

    def _neighbor_rule(self, rel_neighbor):
        """
        Method that should be overridden to change the type of neighborhood calculated.

        By default, this method returns True for all provided coordinates.
        :param list rel_neighbor: the list of relative coordinates around the cell
        :return: True if the relative coordinate should be considered as a neighbor
        """
        return True

    def __neighborhood_generator(self):
        for coordinate in itertools.product(range(-self._radius, self._radius + 1), repeat=len(self._grid_size)):
            if coordinate != (0,) * len(self._grid_size) and self._neighbor_rule(coordinate):
                yield tuple(reversed(coordinate))

    def __neighbors_generator(self, coordinate):
        is_on_edge = self.is_on_edge(coordinate, self._grid_size)
        if self.__edge_rule == EdgeRule.IGNORE_EDGE_CELLS and is_on_edge:
            return
        for rel_n in self._rel_neighbors:
            if is_on_edge:
                n, n_folded = zip(
                    *[(ni + ci, (ni + di + ci) % di) for ci, ni, di in zip(coordinate, rel_n, self._grid_size)]
                )
                if self.__edge_rule == EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS or n == n_folded:
                    yield n_folded
            else:
                yield tuple(map(operator.add, rel_n, coordinate))

    def __lazy_initialize_relative_neighborhood(self, grid_size):
        self._grid_size = grid_size
        if self._rel_neighbors is None:
            self._rel_neighbors = tuple(self.__neighborhood_generator())


class MooreNeighborhood(Neighborhood):
    """Moore defined a neighborhood with a radius applied on a the non euclidean distance to other cells in the grid.
    Example:
        2 dimensions
        C = cell of interest
        N = neighbor of cell
        X = no neighbor of cell

              Radius 1                     Radius 2
           X  X  X  X  X                N  N  N  N  N
           X  N  N  N  X                N  N  N  N  N
           X  N  C  N  X                N  N  C  N  N
           X  N  N  N  X                N  N  N  N  N
           X  X  X  X  X                N  N  N  N  N
    """


class VonNeumannNeighborhood(Neighborhood):
    """Von Neumann defined a neighborhood with a radius applied to Manhatten distance
    (steps between cells without diagonal movement).
    Example:
        2 dimensions
        C = cell of interest
        N = neighbor of cell
        X = no neighbor of cell

              Radius 1                     Radius 2
           X  X  X  X  X                X  X  N  X  X
           X  X  N  X  X                X  N  N  N  X
           X  N  C  N  X                N  N  C  N  N
           X  X  N  X  X                X  N  N  N  X
           X  X  X  X  X                X  X  N  X  X
    """

    def _neighbor_rule(self, rel_neighbor):
        cross_sum = 0
        for coordinate_i in rel_neighbor:
            cross_sum += abs(coordinate_i)
        return cross_sum <= self._radius


class RadialNeighborhood(Neighborhood):
    """Neighborhood with a radius applied to euclidean distance + delta

    Example:
        2 dimensions
        C = cell of interest
        N = neighbor of cell
        X = no neighbor of cell

              Radius 2                     Radius 3
        X  X  X  X  X  X  X          X  X  N  N  N  X  X
        X  X  N  N  N  X  X          X  N  N  N  N  N  X
        X  N  N  N  N  N  X          N  N  N  N  N  N  N
        X  N  N  C  N  N  X          N  N  N  C  N  N  N
        X  N  N  N  N  N  X          N  N  N  N  N  N  N
        X  X  N  N  N  X  X          X  N  N  N  N  N  X
        X  X  X  X  X  X  X          X  X  N  N  N  X  X
    """

    def __init__(self, *args, delta_=0.25, **kwargs):
        self.delta = delta_
        super().__init__(*args, **kwargs)

    def _neighbor_rule(self, rel_neighbor):
        cross_sum = 0
        for coordinate_i in rel_neighbor:
            cross_sum += pow(coordinate_i, 2)
        return math.sqrt(cross_sum) <= (self._radius + self.delta)


class HexagonalNeighborhood(Neighborhood):
    """Defines a Hexagonal neighborhood in a rectangular two dimensional grid:

    Example:
        Von Nexagonal neighborhood in 2 dimensions with radius 1 and 2
        C = cell of interest
        N = neighbor of cell
        X = no neighbor of cell

              Radius 1                     Radius 2
           X   X   X   X   X           X   N   N   N   X
             X   N   N   X               N   N   N   N
           X   N   C   N   X           N   N   C   N   N
             X   N   N   X               N   N   N   N
           X   X   X   X   X           X   N   N   N   X


    Rectangular representation: Radius 1

      Row % 2 == 0            Row % 2 == 1
        N  N  X                 X  N  N
        N  C  N                 N  C  N
        N  N  X                 X  N  N

    Rectangular representation: Radius 2
      Row % 2 == 0            Row % 2 == 1
      X  N  N  N  X           X  N  N  N  X
      N  N  N  N  X           X  N  N  N  N
      N  N  C  N  N           N  N  C  N  N
      N  N  N  N  X           X  N  N  N  N
      X  N  N  N  X           X  N  N  N  X
    """

    def __init__(self, *args, radius=1, **kwargs):
        super().__init__(radius=radius, *args, **kwargs)
        self.__calculate_hexagonal_neighborhood(radius)

    def get_neighbors_coordinates(self, coordinate, grid_size):
        self._rel_neighbors = self._neighbor_lists[coordinate[1] % 2]
        return super().get_neighbors_coordinates(coordinate, grid_size)

    @staticmethod
    def __add_rectangular_neighbours(neighbours, radius, is_odd):
        new_neighbours = []
        for x in range(0, radius + 1):
            if is_odd:
                x -= int(radius / 2)
            else:
                x -= int((radius + 1) / 2)

            for y in range(-radius, radius + 1):
                new_neighbours.append((x, y))
        new_neighbours.extend(neighbours)
        return list(set(new_neighbours))

    @staticmethod
    def __grow_neighbours(neighbours):
        new_neighbours = neighbours[:]
        for n in neighbours:
            new_neighbours.append((n[0], n[1] - 1))
            new_neighbours.append((n[0] - 1, n[1]))
            new_neighbours.append((n[0] + 1, n[1]))
            new_neighbours.append((n[0], n[1] + 1))
        return list(set(new_neighbours))

    def __calculate_hexagonal_neighborhood(self, radius):
        neighbor_lists = [[(0, 0)], [(0, 0)]]
        for radius_i in range(1, radius + 1):
            for i, neighbor in enumerate(neighbor_lists):
                neighbor = HexagonalNeighborhood.__grow_neighbours(neighbor)
                neighbor = HexagonalNeighborhood.__add_rectangular_neighbours(neighbor, radius_i, i % 2 == 1)
                neighbor = sorted(neighbor, key=(lambda ne: [ne[1], ne[0]]))
                neighbor.remove((0, 0))
                neighbor_lists[i] = neighbor
        self._neighbor_lists = neighbor_lists
