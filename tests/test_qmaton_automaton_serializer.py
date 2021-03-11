#!/usr/bindu/python3
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

"""Test file for AutomatonSerializer class"""

import json

from qmaton import Automaton, AutomatonSerializer, State


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule

    def main_rule(self, x, y):
        return DumbAutomaton.STATE


def test_toJSON():
    dab = DumbAutomaton(3, 4)
    out = json.loads(json.dumps(dab, cls=AutomatonSerializer))
    assert "states" in out
    assert out["states"] == [["state", "#000"]]
    assert "grid_size" in out
    assert out["grid_size"] == [3, 4]
    assert "grid" in out
    assert len(out["grid"]) == dab.length
    assert len(out["grid"][0]) == dab.width


def test_fromJSON():
    dab = DumbAutomaton(3, 4)
    out = json.loads(json.dumps(dab, cls=AutomatonSerializer), object_hook=AutomatonSerializer.decode)
    assert out["grid_size"] == dab.grid_size
    assert out["grid"] == dab.grid
