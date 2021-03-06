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

from __future__ import annotations

from dataclasses import dataclass

from .neighborhood import Neighborhood


@dataclass(frozen=True)
class State:
    """State used by the Automaton.

    Each cell of the Automaton can be a State.
    A State is simply a name associated to a color.
    """

    name: str
    color: str


class Automaton:
    """Grid of cells for the cellular automaton.

    An Automaton is defined by a grid of cells, a list of State that can take
    each cell, and one rule that makes the cells change their state at
    each iteration.

    An iteration is calculated thanks to the method `apply_rule()`.

    Attributes:
        grid_size the size of the grid
        states the list of State that can possibly take each cell of the grid
        rule the rule used to calculate an iteration
        grid the grid of cells
        neighborhood the type of neighborhood used
    """

    def __init__(self, length: int = 10, width: int = 10, default_value: State = None):
        """Constructor

        :param int length: the length of the grid
        :param int width: the width of the grid
        :param State default_value: value used to fill the grid
        """
        self.__grid_size: tuple[int, int] = (length, width)
        self.__default_value: State = default_value
        self.states: list[State] = []
        self.rule: callable[[int, int], State] = None
        self.grid: list[list[State]] = self.__init_grid()

    def __str__(self) -> str:
        """Return a string representing the grid.

        The name of the state of all the cells are written, seperated by a space
        for columns and newline for rows.
        """
        s = ""
        for line in self.grid:
            for cell in line:
                s += cell.name + " "
            s += "\n"
        return s

    def __eq__(self, other: Automaton) -> bool:
        return self.states == other.states and self.grid == other.grid

    # Properties

    @property
    def grid_size(self) -> tuple[int, int]:
        """Return the size of the grid in a tuple (length, width)."""
        return self.__grid_size

    @property
    def length(self) -> int:
        return self.__grid_size[0]

    @property
    def width(self) -> int:
        return self.__grid_size[1]

    # Grid management

    def clear_grid(self) -> None:
        """Reset the grid with the default value in all cells."""
        self.grid = self.__init_grid()

    def random_initialize(self) -> None:
        """Initialize each cell of the grid with a random State from the list of states."""
        import random

        if self.states:
            random.seed()
            self.grid = [
                [self.states[random.randrange(len(self.states))] for _ in range(self.width)] for _ in range(self.length)
            ]

    # Run automaton

    def apply_rule(self) -> None:
        """Calculate an iteration of the cellular automaton.

        The setup rule is applied sequencially to each cell.
        """
        new_grid = self.__init_grid()
        # apply rules for each cell
        for i in range(self.length):
            for j in range(self.width):
                new_grid[i][j] = self.rule(i, j)
        self.grid = new_grid

    # Neighborhood utils

    def is_on_edge(self, x: int, y: int, radius: int = 1) -> bool:
        """Tell if the cell in the coordinates (x, y) is on the edge of the grid

        :param int x: x coorindate
        :param int y: y coordinate
        :param int radius: the margin for the grid
        """
        return Neighborhood.is_on_edge((x, y), self.grid_size, radius)

    def count_neighbors(self, neighborhood: Neighborhood, x: int, y: int, states: list[State]) -> int:
        """
        Count the neighbors of the cell grid[coordinate[0]][coordinate[1]] which state is in `states

        :param Neighborhood neighborhood: the neighborhood to use
        :param int x: the coordinate x of the cell
        :param int y: the coordinate y of the cell
        :param list states: the list of states that should be taken in account
        :return: the number of cells in the neighborhood having a state in states
        """
        neighbors = neighborhood.get_neighbors_coordinates((x, y), self.grid_size)
        return sum(1 for n in neighbors if self.grid[n[0]][n[1]] in states)

    # Serialization

    def toJSON(self) -> str:
        """Return a JSON string representation of the automaton."""
        import json

        from qmaton import AutomatonSerializer

        return json.dumps(self, indent=4, cls=AutomatonSerializer)

    @classmethod
    def fromJSON(cls, json_str: str) -> Automaton:
        """Create an automaton from the JSON string."""
        import json

        from qmaton import AutomatonSerializer

        o = json.loads(json_str, object_hook=AutomatonSerializer.decode)
        automaton = cls(o["grid_size"][0], o["grid_size"][1])
        automaton.grid = o["grid"]
        return automaton

    # Private methods

    def __init_grid(self) -> list[list[State]]:
        return [[self.__default_value for _ in range(self.width)] for _ in range(self.length)]
