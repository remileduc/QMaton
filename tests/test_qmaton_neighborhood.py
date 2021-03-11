#!/usr/bin/python3
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

"""Test file for Neighborhood classes"""


from pytest import mark
from qmaton import (
    EdgeRule,
    HexagonalNeighborhood,
    MooreNeighborhood,
    Neighborhood,
    RadialNeighborhood,
    VonNeumannNeighborhood,
)


@mark.parametrize(
    ("coordinate", "expected_neighborhood"),
    (
        ((0, 0), ((1, 0), (0, 1), (1, 1))),
        ((0, 1), ((0, 0), (1, 0), (1, 1), (0, 2), (1, 2))),
        ((1, 1), ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2))),
        ((2, 2), ((1, 1), (2, 1), (1, 2))),
    ),
)
def test_ignore_missing_neighbors(coordinate, expected_neighborhood):
    neighborhood = MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS)
    actual_neighborhood = neighborhood.get_neighbors_coordinates(coordinate, (3, 3))
    assert tuple(actual_neighborhood) == expected_neighborhood


@mark.parametrize(
    ("coordinate", "expected_neighborhood"),
    (
        ((0, 0), ()),
        ((0, 1), ()),
        ((2, 0), ()),
        ((1, 1), ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2))),
        ((2, 2), ()),
    ),
)
def test_ignore_edge_cells(coordinate, expected_neighborhood):
    neighborhood = MooreNeighborhood()
    actual_neighborhood = neighborhood.get_neighbors_coordinates(coordinate, (3, 3))
    assert tuple(actual_neighborhood) == expected_neighborhood


@mark.parametrize(
    ("coordinate", "expected_neighborhood"),
    (
        ((0, 0), ((2, 2), (0, 2), (1, 2), (2, 0), (1, 0), (2, 1), (0, 1), (1, 1))),
        ((1, 1), ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2))),
        ((2, 2), ((1, 1), (2, 1), (0, 1), (1, 2), (0, 2), (1, 0), (2, 0), (0, 0))),
    ),
)
def test_cyclic_dimensions(coordinate, expected_neighborhood):
    neighborhood = MooreNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    actual_neighborhood = neighborhood.get_neighbors_coordinates(coordinate, (3, 3))
    assert tuple(actual_neighborhood) == expected_neighborhood


@mark.parametrize(
    ("coordinate", "result"),
    (
        ((0, 0), True),
        ((0, 1), True),
        ((0, 2), True),
        ((0, 3), True),
        ((1, 0), True),
        ((1, 1), False),
        ((1, 2), False),
        ((1, 3), True),
        ((2, 0), True),
        ((2, 1), False),
        ((2, 2), False),
        ((2, 3), True),
        ((3, 0), True),
        ((3, 1), False),
        ((3, 2), False),
        ((3, 3), True),
        ((4, 0), True),
        ((4, 1), True),
        ((4, 2), True),
        ((4, 3), True),
    ),
)
def test_is_on_edge(coordinate, result):
    assert Neighborhood.is_on_edge(coordinate, (5, 4), 1) is result


def test_von_neumann_r1():
    neighborhood = VonNeumannNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    actual_neighborhood = neighborhood.get_neighbors_coordinates((1, 1), (3, 3))
    assert tuple(actual_neighborhood) == ((1, 0), (0, 1), (2, 1), (1, 2))


def test_von_neumann_r2():
    neighborhood = VonNeumannNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS, radius=2)
    actual_neighborhood = neighborhood.get_neighbors_coordinates((2, 2), (5, 5))
    assert tuple(actual_neighborhood) == (
        (2, 0),
        (1, 1),
        (2, 1),
        (3, 1),
        (0, 2),
        (1, 2),
        (3, 2),
        (4, 2),
        (1, 3),
        (2, 3),
        (3, 3),
        (2, 4),
    )


def test_von_neumann_d3():
    neighborhood = VonNeumannNeighborhood(EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    actual_neighborhood = neighborhood.get_neighbors_coordinates((1, 1, 1), (3, 3, 3))
    assert tuple(actual_neighborhood) == (
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (2, 1, 1),
        (1, 2, 1),
        (1, 1, 2),
    )


def test_radial():
    neighborhood = RadialNeighborhood(radius=2)
    actual_neighborhood = neighborhood.get_neighbors_coordinates((2, 2), (5, 5))
    assert tuple(actual_neighborhood) == (
        (1, 0),
        (2, 0),
        (3, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (0, 2),
        (1, 2),
        (3, 2),
        (4, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (1, 4),
        (2, 4),
        (3, 4),
    )


@mark.parametrize(
    ("coordinate", "result"),
    (
        (
            (0, 0),
            (
                (9, 8),
                (0, 8),
                (1, 8),
                (8, 9),
                (9, 9),
                (0, 9),
                (1, 9),
                (2, 9),
                (8, 0),
                (9, 0),
                (1, 0),
                (2, 0),
                (8, 1),
                (9, 1),
                (0, 1),
                (1, 1),
                (2, 1),
                (9, 2),
                (0, 2),
                (1, 2),
            ),
        ),
        (
            (1, 1),
            (
                (0, 9),
                (1, 9),
                (2, 9),
                (9, 0),
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (9, 1),
                (0, 1),
                (2, 1),
                (3, 1),
                (9, 2),
                (0, 2),
                (1, 2),
                (2, 2),
                (3, 2),
                (0, 3),
                (1, 3),
                (2, 3),
            ),
        ),
    ),
)
def test_radial_neighbor_coords(coordinate, result):
    neighborhood = RadialNeighborhood(edge_rule=EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS, radius=2)
    neighbor_coords = neighborhood.get_neighbors_coordinates(coordinate, (10, 10))
    assert tuple(neighbor_coords) == result


@mark.parametrize(
    ("coordinate", "expected_neighborhood"),
    (
        (
            (2, 2),
            (
                (1, 0),
                (2, 0),
                (3, 0),
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (0, 2),
                (1, 2),
                (3, 2),
                (4, 2),
                (0, 3),
                (1, 3),
                (2, 3),
                (3, 3),
                (1, 4),
                (2, 4),
                (3, 4),
            ),
        ),
        (
            (2, 3),
            (
                (1, 1),
                (2, 1),
                (3, 1),
                (1, 2),
                (2, 2),
                (3, 2),
                (4, 2),
                (0, 3),
                (1, 3),
                (3, 3),
                (4, 3),
                (1, 4),
                (2, 4),
                (3, 4),
                (4, 4),
                (1, 5),
                (2, 5),
                (3, 5),
            ),
        ),
    ),
)
def test_hexagonal(coordinate, expected_neighborhood):
    neighborhood = HexagonalNeighborhood(radius=2)
    actual_neighborhood = neighborhood.get_neighbors_coordinates(coordinate, (6, 6))
    assert tuple(actual_neighborhood) == expected_neighborhood


@mark.parametrize(
    ("dimension", "expected"),
    (
        (1, ((0,), (2,))),
        (2, ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2))),
        (
            3,
            (
                (0, 0, 0),
                (1, 0, 0),
                (2, 0, 0),
                (0, 1, 0),
                (1, 1, 0),
                (2, 1, 0),
                (0, 2, 0),
                (1, 2, 0),
                (2, 2, 0),
                (0, 0, 1),
                (1, 0, 1),
                (2, 0, 1),
                (0, 1, 1),
                (2, 1, 1),
                (0, 2, 1),
                (1, 2, 1),
                (2, 2, 1),
                (0, 0, 2),
                (1, 0, 2),
                (2, 0, 2),
                (0, 1, 2),
                (1, 1, 2),
                (2, 1, 2),
                (0, 2, 2),
                (1, 2, 2),
                (2, 2, 2),
            ),
        ),
    ),
)
def test_get_neighbor_coordinates(dimension, expected):
    n = MooreNeighborhood(edge_rule=EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS)
    assert tuple(n.get_neighbors_coordinates((1,) * dimension, (3,) * dimension)) == expected
