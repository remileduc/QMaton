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

"""Test file for FileVisualizer class"""

import os
from pathlib import Path

from qmaton import Automaton, State
from visualizer import FileVisualizer


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule

    def main_rule(self, x, y):
        return DumbAutomaton.STATE


def test_init(tmp_path):
    assert not FileVisualizer().file
    file = tmp_path / "test_init.tmp"
    Path(file).touch()
    assert os.path.exists(file)
    assert FileVisualizer(file).file == file
    assert not os.path.exists(file)


def test_draw_nofile(capsys):
    dab = DumbAutomaton(6, 3)
    fv = FileVisualizer()
    fv.draw(dab)
    assert capsys.readouterr().out == (str(dab) + "\n")


def test_draw_withfile(tmp_path):
    dab = DumbAutomaton(6, 3)
    file = tmp_path / "test_draw_withfile.tmp"
    fv = FileVisualizer(file)
    fv.draw(dab)
    fv.draw(dab)
    with open(file, "r") as f:
        assert f.read() == (str(dab) + "\n") * 2
