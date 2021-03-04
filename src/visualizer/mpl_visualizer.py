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

"""Show the steps in a matplotlib diagram."""


from matplotlib import pyplot as plt


class MPLVisualizer:
    """Show the steps in a matplotlib diagram."""

    def __init__(self, width, length):
        self.figure = plt.figure()
        plt.ion()
        plt.xlim(-1, width + 1)
        plt.ylim(-1, length + 1)

    def draw(self, automaton):
        """Callback for the AutomatonRunner."""
        class __State:
            def __init__(self, color):
                self.color = color
                self.x = []
                self.y = []

        states = {}
        grid = automaton.grid
        for i in range(automaton.length):
            for j in range(automaton.width):
                if grid[i][j].name not in states:
                    states[grid[i][j].name] = __State(grid[i][j].color)
                states[grid[i][j].name].x.append(i)
                states[grid[i][j].name].y.append(j)

        plt.clf()
        for value in states.values():
            plt.plot(value.x, value.y, 's', color=value.color)
        self.figure.canvas.draw()


if __name__ == "__main__":
    from automaton import GameOfLife
    from qmaton import Automaton, AutomatonRunner

    ca = GameOfLife(10, 10)

    ca.random_initialize()
    ar = AutomatonRunner(10, 100)
    av = MPLVisualizer(ca.width, ca.length)

    #ar.launch(ca, av.draw)
    av.draw(ca)

