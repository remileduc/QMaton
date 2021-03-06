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

Launch the automaton. You can change the automaton and the visualizer used below.
"""


from automaton import GameOfLife
from PyQt5.QtWidgets import QApplication
from qtui import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    m = MainWindow(GameOfLife)
    if m._automaton is None:
        gol = GameOfLife(10, 10)
        gol.random_initialize()
        m.set_automaton(gol)

    m.show()
    app.exec_()
