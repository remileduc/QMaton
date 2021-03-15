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

"""Test file for AutomatonHistory class"""

from pytest import raises
from qmaton import Automaton, AutomatonHistory, State


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule

    def main_rule(self, x, y):
        return "lol"


def test_init():
    ah = AutomatonHistory()
    assert ah.history_size == 10000
    assert len(ah) == 0
    assert not ah
    assert ah.current_index == -1


def test_operator_get():
    ah = AutomatonHistory()
    lol = []
    ah.append(lol)
    ah.append("lil")
    assert ah[0] == lol
    assert ah[0] is not lol
    assert ah[1] == "lil"
    with raises(IndexError):
        ah[2]


def test_operator_set():
    ah = AutomatonHistory()
    ah.append("lol")
    assert ah[0] == "lol"
    tmp = [[1, 2, 3], [10, 11, 12]]
    ah[0] = tmp
    assert ah[0] == tmp
    assert ah[0] is not tmp
    tmp[0] = 0
    assert ah[0] != tmp
    with raises(IndexError):
        ah[1] = "dumb"


def test_operator_len():
    ah = AutomatonHistory()
    assert len(ah) == 0
    ah.append("lol")
    assert len(ah) == 1
    for _ in range(100):
        ah.append(0)
    assert len(ah) == 101


def test_operator_bool():
    ah = AutomatonHistory()
    assert not ah
    ah.append("lol")
    assert bool(ah)
    ah.clear()
    assert not ah


def test_history_size():
    ah = AutomatonHistory()
    assert ah.history_size == 10000
    ah = AutomatonHistory(153)
    assert ah.history_size == 153


def test_current_index():
    ah = AutomatonHistory()
    assert ah.current_index == -1
    ah.append("lol")
    assert ah.current_index == 0
    for _ in range(10):
        ah.append(2)
    assert ah.current_index == 10
    ah.move_to(7)
    assert ah.current_index == 7
    ah.move_to(9)
    assert ah.current_index == 9
    ah.clear_after(5)
    assert ah.current_index == 5
    ah.clear()
    assert ah.current_index == -1


def test_remaining_steps():
    ah = AutomatonHistory()
    assert ah.remaining_steps == 0
    for _ in range(10):
        ah.append(2)
    assert ah.remaining_steps == 0
    ah.move_to(6)
    assert ah.remaining_steps == 3
    ah.move_to(8)
    assert ah.remaining_steps == 1
    ah.clear_after(5)
    assert ah.remaining_steps == 0
    ah.clear()
    assert ah.remaining_steps == 0


def test_get():
    ah = AutomatonHistory()
    with raises(IndexError):
        ah.get()
    for i in range(10):
        ah.append(i)
        assert ah.get() == i
    ah.move_to(4)
    assert ah.get() == 4
    ah.move_forward()
    assert ah.get() == 5


def test_append():
    ah = AutomatonHistory(153)
    tmp = [[1, 2, 3], [10, 11, 12]]
    assert len(ah) == 0
    ah.append(tmp)
    assert ah.get() == tmp
    assert len(ah) == 1
    assert ah.get() == tmp
    assert ah.get() is not tmp
    for _ in range(152):
        ah.append(tmp)
    assert len(ah) == 153
    assert ah.get() == tmp
    assert ah.get() is not tmp
    assert ah.current_index == 152
    with raises(IndexError):
        ah.append(tmp)
    ah.move_to(3)
    ah.append("lol")
    assert len(ah) == 5


def test_append_automaton_state():
    dab = DumbAutomaton(10, 10)
    ah = AutomatonHistory()
    ah.append_automaton_state(dab)
    assert ah.get() == dab.grid
    assert len(ah) == 1
    assert ah.get() == dab.grid
    assert ah.get() is not dab.grid
    dab.grid[2][3] = None
    ah.append_automaton_state(dab)
    assert len(ah) == 2
    assert ah[0] != dab.grid
    assert ah[1] == dab.grid
    assert ah[1] is not dab.grid
    assert ah[0] != ah[1]


def test_clear():
    ah = AutomatonHistory(10)
    assert len(ah) == 0
    ah.clear()
    assert len(ah) == 0
    for _ in range(10):
        ah.append(2)
    with raises(IndexError):
        ah.append(2)
    ah.clear()
    assert len(ah) == 0
    with raises(IndexError):
        ah[0]
    ah.append(2)
    assert len(ah) == 1


def test_clear_after():
    ah = AutomatonHistory()
    for _ in range(1000):
        ah.append(2)
    assert len(ah) == 1000
    ah.clear_after(2000)
    assert len(ah) == 1000
    ah.clear_after(100)
    assert len(ah) == 101
    assert ah.get() == 2
    with raises(IndexError):
        ah[101]
    ah.move_to(90)
    assert ah.current_index == 90
    ah.clear_after()
    assert len(ah) == 91
    ah.clear_after(0)
    assert len(ah) == 1
    assert ah[0] == 2


def test_move_backward():
    ah = AutomatonHistory()
    for i in range(10):
        ah.append(i)
    assert ah.get() == 9
    assert ah.move_backward(3) == 6
    assert ah.get() == 6
    assert ah.remaining_steps == 3
    assert ah.current_index == 6
    for i in range(6):
        assert ah.move_backward() == 5 - i
        assert ah.get() == 5 - i
    assert ah.current_index == 0


def test_move_forward():
    ah = AutomatonHistory()
    for i in range(10):
        ah.append(i)
    assert ah.get() == 9
    assert ah.move_backward(9) == 0
    assert ah.get() == 0
    assert ah.move_forward(3) == 3
    assert ah.remaining_steps == 6
    assert ah.current_index == 3
    for i in range(6):
        assert ah.move_forward() == 4 + i
        assert ah.get() == 4 + i
    assert ah.current_index == 9


def test_move_to():
    ah = AutomatonHistory()
    for i in range(10):
        ah.append(i)
    assert ah.get() == 9
    assert ah.move_to(0) == 0
    assert ah.get() == 0
    assert ah.move_to(3) == 3
    assert ah.remaining_steps == 6
    assert ah.current_index == 3
    for i in range(10):
        assert ah.move_to(i) == i
        assert ah.get() == i
    assert ah.current_index == 9
