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

"""Automaton class, represneting the grid of cells."""


import random
from collections import namedtuple
from copy import deepcopy


class Automaton:
    """"Grid of cells for the cellular automaton.

    An Automaton is defined by a grid of cells, a list of State that can take
    each cell, and a list of rules that makes the cells change their state at
    each iteration.

    An iteration is calculated thanks to the method `apply_rules()`.

    Attributes:
        width the width of the grid
        length the length of the grid
        states the list of State that can possibly take each cell of the grid
        rules the list of rules used to calculate an iteration
        grid the grid of cells
    """

    State = namedtuple('State', ['name', 'color'])
    """State used by the Automaton.

    Each cell of the Automaton can be a State.
    A State is simply a name associated to a color.
    """

    def __init__(self, width=10, length=10, default_value=None):
        """Constructor

        :param int width: the width of the grid
        :param int length: the length of the string
        """
        self.__width = width
        self.__length = length
        self.states = []
        self.rules = []
        self.grid = [[default_value for _ in range(width)] for _ in range(length)]

    def __str__(self):
        """Return a string representing the grid.

        The name of the state of all the cells are written, seperated by a space
        for columns and newline for rows.
        """
        s = ''
        for line in self.grid:
            for cell in line:
                s += cell.name + ' '
            s += '\n'
        return s

    @property
    def width(self):
        return self.__width

    @property
    def length(self):
        return self.__length

    def random_initialize(self):
        """Initialize each cell of the grid with a random State from the list of states."""
        if self.states:
            random.seed()
            self.grid = [[self.states[random.randrange(len(self.states))]
                          for _ in range(self.width)] for _ in range(self.length)]

    def apply_rules(self):
        """Calculate an iteration of the cellular automaton.

        Each rule defined in the list of rules is applied sequencially to each cell.
        This means that the last rule will always prevail.
        """
        new_grid = deepcopy(self.grid)
        # apply rules for each cell
        for i in range(self.length):
            for j in range(self.width):
                for rule in self.rules:
                    new_grid[i][j] = rule(new_grid, i, j)
        self.grid = new_grid
