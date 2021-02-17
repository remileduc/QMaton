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


from qmaton import Automaton, neighborhood


class GameOfLife:
    """Game of life example.

    See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """

    LIFE = Automaton.State('Life ', '#000')
    """Life state, black"""
    DEATH = Automaton.State('Death', '#FFF')
    """Death state, white"""

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_death_cell(grid, x, y):
        if grid[x][y] == GameOfLife.DEATH and neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE) == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_life_cell(grid, x, y):
        alive = neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE)
        if alive == 2 or alive == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH

    @staticmethod
    def get_automaton(width, length):
        """Create an Automaton, already set up with rules and states.

        :param int width: the width of the grid of the automaton
        :param int length: the length of the grid of the automaton
        :return Automaton: an automaton with states and rules
        """
        ca = Automaton(width, length, GameOfLife.DEATH)
        ca.rules = [GameOfLife.rule_death_cell, GameOfLife.rule_life_cell]
        ca.states = [GameOfLife.LIFE, GameOfLife.DEATH]
        return ca
