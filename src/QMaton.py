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

"""Main entry for QMaton.

Launch the automaton. You can change the automaton and the visulaizer used below.
"""


from automaton import GameOfLife
from qmaton import Automaton, AutomatonRunner
from visualizer import FileVisualizer


if __name__ == "__main__":
    ca = GameOfLife(10, 10)

    ca.random_initialize()
    ar = AutomatonRunner(10, 100)
    #av = FileVisualizer("test.txt")
    av = FileVisualizer()

    ar.launch(ca, av.draw)
    av.draw(ca)
