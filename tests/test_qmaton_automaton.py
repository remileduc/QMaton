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

"""Test file for Automaton class"""

from pytest import mark
from qmaton import Automaton, EdgeRule, MooreNeighborhood, State


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule
        self.rule_executed_cpt = 0

    def main_rule(self, x, y):
        self.rule_executed_cpt += 1
        return "lol"


def test_init():
    dab = DumbAutomaton(2, 3)
    # size
    assert dab.grid_size == (2, 3)
    assert dab.width == 3
    assert dab.length == 2
    assert len(dab.grid) == 2
    assert len(dab.grid[0]) == 3
    # states
    assert dab.states == [DumbAutomaton.STATE]
    assert all(s is DumbAutomaton.STATE for line in dab.grid for s in line)


def test_str():
    dab = DumbAutomaton(2, 3)
    result = "state state state \n" "state state state \n"
    assert str(dab) == result


def test_eq():
    dab = DumbAutomaton(2, 3)
    dab2 = DumbAutomaton(2, 3)
    dab2.rule = None
    assert dab == dab2


def test_random_initialize():
    dab = DumbAutomaton(2, 3)
    assert all(s is DumbAutomaton.STATE for line in dab.grid for s in line)
    dab.grid = [[None for _ in line] for line in dab.grid]
    assert all(s is None for line in dab.grid for s in line)
    dab.states = []
    dab.random_initialize()
    assert all(s is None for line in dab.grid for s in line)
    dab.states = [DumbAutomaton.STATE]
    dab.random_initialize()
    assert all(s is DumbAutomaton.STATE for line in dab.grid for s in line)


def test_apply_rule():
    dab = DumbAutomaton(2, 3)
    dab.apply_rule()
    assert dab.rule_executed_cpt == 6
    assert all(s == "lol" for line in dab.grid for s in line)


@mark.parametrize(
    ("coordinate", "result"),
    (
        ((0, 0), True),
        ((0, 1), True),
        ((0, 2), True),
        ((0, 3), True),
        ((0, 4), True),
        ((0, 5), True),
        ((1, 0), True),
        ((1, 1), True),
        ((1, 2), True),
        ((1, 3), True),
        ((1, 4), True),
        ((1, 5), True),
        ((2, 0), True),
        ((2, 1), True),
        ((2, 2), False),
        ((2, 3), False),
        ((2, 4), True),
        ((2, 5), True),
        ((3, 0), True),
        ((3, 1), True),
        ((3, 2), True),
        ((3, 3), True),
        ((3, 4), True),
        ((3, 5), True),
        ((4, 0), True),
        ((4, 1), True),
        ((4, 2), True),
        ((4, 3), True),
        ((4, 4), True),
        ((4, 5), True),
    ),
)
def test_is_on_edge(coordinate, result):
    assert Automaton(5, 6).is_on_edge(*coordinate, 2) == result


@mark.parametrize(
    ("coordinate", "result"),
    (((0, 0), 3), ((0, 1), 5), ((1, 1), 8), ((2, 2), 5), ((3, 2), 3)),
)
def test_count_neighbors(coordinate, result):
    dab = DumbAutomaton(4, 3)
    neighborhood = MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS)
    assert dab.count_neighbors(neighborhood, *coordinate, (DumbAutomaton.STATE,)) == result


def test_JSON():
    dab = DumbAutomaton(2, 3)
    assert dab == DumbAutomaton.fromJSON(dab.toJSON())
