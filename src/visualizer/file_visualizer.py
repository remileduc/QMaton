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

"""Print the steps in the console, or save it in a file."""


import os

from qmaton import Automaton


class FileVisualizer:
    """Print the steps in the console, or save it in a file.

    Attributes
        file the file where to write results. If not set, print on console.
    """

    def __init__(self, file: str = ""):
        self.file: str = file
        if file and os.path.exists(file):
            os.remove(file)

    def draw(self, automaton: Automaton) -> None:
        """Callback for the AutomatonRunner."""
        if not self.file:
            print(automaton)
            return
        with open(self.file, "a") as f:
            f.write(str(automaton) + "\n")
