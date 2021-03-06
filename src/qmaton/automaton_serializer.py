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

"""Automaton serializer, export / import automaton state from / to JSON."""


from json import JSONEncoder

from qmaton import Automaton, State


class AutomatonSerializer(JSONEncoder):
    def default(self, o):
        if not isinstance(o, Automaton):
            return super().default(o)
        return {
            "states": o.states,
            "grid_size": o.grid_size,
            "grid": [[state.name for state in line] for line in o.grid]
        }

    @staticmethod
    def decode(o):
        states = {}
        grid_size = (0, 0)
        grid = [[]]
        if "states" in o:
            states = {s[0]: State(*s) for s in o["states"]}
        if "grid_size" in o:
            grid_size = tuple(o["grid_size"])
        if "grid" in o:
            grid = [[states[s] for s in line] for line in o["grid"]]
        return {
            "grid_size": grid_size,
            "grid": grid
        }
