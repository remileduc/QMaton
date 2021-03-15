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

# flake8: noqa

"""QMaton main module.

This module contains all the logic for running a cellular automaton:

- Automaton class is the grid
- AutomatonRunner class allow to run the automaton multiple times
- neighborhood is a module with utils functions for neighborhood computation
"""


from .automaton import *
from .automaton_history import *
from .automaton_runner import *
from .automaton_serializer import *
from .neighborhood import *
