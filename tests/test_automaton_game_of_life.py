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

"""Test file for GameOfLife class"""

from copy import deepcopy
from unittest.mock import MagicMock

from automaton import GameOfLife
from pytest import fixture, mark
from qmaton import MooreNeighborhood

# Base test
# · is DEATH
# 0 is LIFE
#
# Step 1     Step 2     Step 3
#
#  ·····      ·····      ·····
#  ·00··      ·00··      ·00··
#  ·00··      ·00··      ·00··
#  ·····  ->  ·····  ->  ·····  ->  ...
#  ·00··      ·····      ·····
#  ····0      ·00·0      ·00·0
#  0··00      0··00      0··00
L = GameOfLife.LIFE
D = GameOfLife.DEATH
grid1 = [
    [D, D, D, D, D],
    [D, L, L, D, D],
    [D, L, L, D, D],
    [D, D, D, D, D],
    [D, L, L, D, D],
    [D, D, D, D, L],
    [L, D, D, L, L],
]
grid2 = [
    [D, D, D, D, D],
    [D, L, L, D, D],
    [D, L, L, D, D],
    [D, D, D, D, D],
    [D, D, D, D, D],
    [D, L, L, D, L],
    [L, D, D, L, L],
]


@fixture
def gollum():
    gol = GameOfLife(7, 5)
    gol.grid = deepcopy(grid1)
    return gol


@fixture
def golres():
    gol = GameOfLife(7, 5)
    gol.grid = deepcopy(grid2)
    return gol


def test_init():
    gol = GameOfLife(2, 3)
    assert gol.grid_size == (2, 3)
    assert gol.rule == gol.main_rule
    assert isinstance(gol.neighborhood, MooreNeighborhood)
    # states
    assert len(gol.states) == 2
    assert GameOfLife.LIFE in gol.states
    assert GameOfLife.DEATH in gol.states
    assert all(s is GameOfLife.DEATH for line in gol.grid for s in line)


@mark.parametrize(
    ("coordinate", "result"),
    (((0, 0), D), ((1, 1), L), ((4, 2), L), ((5, 2), L), ((5, 3), D)),
)
def test_rule_death_cell(gollum, coordinate, result):
    assert gollum.rule_death_cell(*coordinate) == result


@mark.parametrize(
    ("coordinate", "result"),
    (((0, 0), D), ((1, 1), L), ((4, 2), D), ((5, 2), D), ((5, 3), D)),
)
def test_rule_life_cell(gollum, coordinate, result):
    assert gollum.rule_life_cell(*coordinate) == result


@mark.parametrize(
    ("coordinate", "result"),
    (((0, 0), D), ((1, 1), L), ((4, 2), L), ((5, 3), D), ((6, 4), L)),
)
def test_main_rule(gollum, coordinate, result):
    gollum.rule_death_cell = MagicMock(return_value=D)
    gollum.rule_life_cell = MagicMock(return_value=L)

    assert gollum.main_rule(*coordinate) == result


def test_main_rule_none(gollum):
    gollum.grid[2][1] = None
    assert gollum.main_rule(2, 1) is None


def test_apply_rule(gollum, golres):
    assert gollum != golres
    for i in range(3):
        gollum.apply_rule()
    assert gollum == golres
