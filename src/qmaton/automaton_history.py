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

"""AutomatonHistory class, holds the different calculated steps of an automaton."""

from copy import deepcopy
from typing import List

from .automaton import Automaton, State

Grid = List[List[State]]
"""The grid of an automaton."""


class AutomatonHistory:
    """History for Cellular Automatons.

    This class holds grids of automatons, so you can go back to a previously calculated step easily.
    AutomatonHistory automatically stores deep copies of the provided grid.
    It is best used with an AutomatonRunner.
    """

    def __init__(self, history_size: int = 10000):
        """Constructor

        :param int history_size: the size of the history. Over this, it won't be possible to store more steps
        """
        self.__history_size: int = history_size
        self.__history: list[Grid] = []
        self.__current: int = -1

    # List style

    def __getitem__(self, idx: int) -> Grid:
        """Return the grid at the given position in the history."""
        return deepcopy(self.__history[idx])

    def __setitem__(self, idx: int, grid: Grid):
        """Creates a deep copy of the given grid and stores it at the given position."""
        self.__history[idx] = deepcopy(grid)

    def __len__(self) -> int:
        return len(self.__history)

    def __bool__(self) -> bool:
        return bool(self.__history)

    # Properties

    @property
    def history_size(self) -> int:
        """Return the maximum size the history can take."""
        return self.__history_size

    @property
    def current_index(self) -> int:
        """Return the current index in the history."""
        return self.__current

    @property
    def remaining_steps(self) -> int:
        """Return the number of steps remaining to arrive to latest.
        Number of time you can safely call move_forward(1).
        """
        return len(self.__history) - self.__current - 1

    # List management

    def get(self) -> Grid:
        """Return last saved state.

        Use operator [i] to access specific step.
        """
        return self[self.__current]

    def append(self, grid: Grid) -> None:
        """Creates a deep copy of the grid and append it to the history.

        :param grid: the grid to add in the history
        """
        if self.remaining_steps > 0:
            self.clear_after()
        if len(self.__history) >= self.__history_size:
            raise IndexError(f"Maximum history size, can't store more steps: {self.__history_size}.")
        self.__history.append(deepcopy(grid))
        self.__current += 1

    def append_automaton_state(self, automaton: Automaton) -> None:
        """Creates a deep copy of the grid of the given automaton and append it to the history.

        This method can safely be used as callback for an AutomatonRunner.
        :param Automaton automaton: the automaton from which extract the grid and save its state
        :return: the deep copy of the automaton's grid
        """
        self.append(automaton.grid)

    def clear(self) -> None:
        """Clear the history."""
        self.__history.clear()
        self.__current = -1

    def clear_after(self, idx: int = -1) -> None:
        """Clear the history after the given index.

        The given index is kept: automatonHistory[idx] is still valid after the call.
        :param int idx: the index from which remove the history, default is current_index
        """
        if idx < 0:
            idx = self.__current
        if idx >= len(self.__history) - 1:
            return
        self.__history[:] = self.__history[: idx + 1]
        if self.__current > idx:
            self.__current = idx

    # Navigation

    def move_backward(self, step: int = 1) -> Grid:
        """Move current_index of X steps back.

        :return: the saved state at the new current_index.
        """
        self.__current -= step
        return self[self.__current]

    def move_forward(self, step: int = 1) -> Grid:
        """Move current_index of X steps forward.

        :return: the saved state at the new current_index.
        """
        self.__current += step
        return self[self.__current]

    def move_to(self, idx: int) -> Grid:
        """Move current_index to idx.

        :return: the saved state at the new current_index.
        """
        self.__current = idx
        return self[self.__current]
