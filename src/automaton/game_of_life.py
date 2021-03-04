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

"""Game of life example."""


from qmaton import Automaton, MooreNeighborhood, State


class GameOfLife(Automaton):
    """Game of life example.

    See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """

    LIFE = State('Life ', '#000')
    """Life state, black"""
    DEATH = State('Death', '#FFF')
    """Death state, white"""

    def __init__(self, width, length):
        """Create an Automaton, already set up with rules and states.

        :param int width: the width of the grid of the automaton
        :param int length: the length of the grid of the automaton
        """
        super().__init__(width, length, GameOfLife.DEATH)
        self.states = [GameOfLife.LIFE, GameOfLife.DEATH]
        self.rule = self.main_rule
        self.neighborhood = MooreNeighborhood()

    def main_rule(self, x, y):
        if self.grid[x][y] == GameOfLife.DEATH:
            return self.rule_death_cell(x, y)
        elif self.grid[x][y] == GameOfLife.LIFE:
            return self.rule_life_cell(x, y)
        return self.grid[x][y]

    def rule_death_cell(self, x, y):
        if self.grid[x][y] == GameOfLife.DEATH and self.count_neighbors(self.neighborhood, x, y, (GameOfLife.LIFE,)) == 3:
            return GameOfLife.LIFE
        return self.grid[x][y]

    def rule_life_cell(self, x, y):
        if self.grid[x][y] != GameOfLife.LIFE:
            return self.grid[x][y]
        alive = self.count_neighbors(self.neighborhood, x, y, (GameOfLife.LIFE,))
        if alive == 2 or alive == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from visualizer import QtVisualizer

    app = QApplication([])

    ca = GameOfLife(30, 30)

    # Initialize
    ca.random_initialize()

    av = QtVisualizer(ca)

    av.show()
    app.exec_()
