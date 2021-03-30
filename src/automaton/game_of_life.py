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


from qmaton import Automaton, MooreNeighborhood, Neighborhood, State


class GameOfLife(Automaton):
    """Game of life example.

    See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """

    LIFE = State("Life ", "#000")
    """Life state, black"""
    DEATH = State("Death", "#FFF")
    """Death state, white"""

    def __init__(self, length: int = 10, width: int = 10):
        """Create an Automaton, already set up with rules and states.

        :param int length: the length of the grid of the automaton
        :param int width: the width of the grid of the automaton
        """
        super().__init__(length, width, GameOfLife.DEATH)
        self.states: list[State] = [GameOfLife.LIFE, GameOfLife.DEATH]
        self.rule: callable[[int, int], State] = self.main_rule
        self.neighborhood: Neighborhood = MooreNeighborhood()

    def main_rule(self, x: int, y: int) -> State:
        if self.is_on_edge(x, y):
            return self.grid[x][y]
        if self.grid[x][y] == GameOfLife.DEATH:
            return self.rule_death_cell(x, y)
        elif self.grid[x][y] == GameOfLife.LIFE:
            return self.rule_life_cell(x, y)
        return self.grid[x][y]

    def rule_death_cell(self, x: int, y: int) -> State:
        if (
            self.grid[x][y] == GameOfLife.DEATH
            and self.count_neighbors(self.neighborhood, x, y, (GameOfLife.LIFE,)) == 3
        ):
            return GameOfLife.LIFE
        return self.grid[x][y]

    def rule_life_cell(self, x: int, y: int) -> State:
        if self.grid[x][y] != GameOfLife.LIFE:
            return self.grid[x][y]
        alive = self.count_neighbors(self.neighborhood, x, y, (GameOfLife.LIFE,))
        if alive == 2 or alive == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH
