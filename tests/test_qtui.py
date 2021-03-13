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

"""Test file for qtui module"""

from PyQt5.QtWidgets import QApplication
from pytest import fixture
from qmaton import Automaton, State
from qtui import MainWindow


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule

    def main_rule(self, x, y):
        return self.grid[x][y]


@fixture(autouse=True, scope="module")
def application():
    return QApplication([])


def test_MainWindow_init(tmp_path):
    m = MainWindow()
    assert m._automaton is None


def test_MainWindow_set_automaton(capsys):
    dab = DumbAutomaton(6, 3)
    m = MainWindow()
    m.set_automaton(dab)
    assert m._automaton is dab
