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

"""Test file for AutomatonRunner class"""


from time import sleep, time

from qmaton import Automaton, AutomatonRunner, State


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule
        self.rule_executed_cpt = 0
        self.callback_cpt = 0

    def main_rule(self, x, y):
        self.rule_executed_cpt += 1
        return "lol"

    def callback(self, _):
        self.callback_cpt += 1

    def callback_long(self, _):
        sleep(0.1)
        self.callback_cpt += 1


def test_init():
    ar = AutomatonRunner(6, 3)
    assert ar.nb_iter == 6
    assert ar.sleep_time == 1 / 3


def test_launch():
    dab = DumbAutomaton(2, 3)
    ar = AutomatonRunner(6, 12)

    time_before = time()
    ar.launch(dab, dab.callback)
    time_after = time()
    total_time = time_after - time_before

    assert dab.rule_executed_cpt == 36  # 2 * 3 * 6
    assert dab.callback_cpt == 6
    assert total_time > 0.5  # 12 operations per seconds, we do 6, so 0.5 seconds
    assert total_time < 0.6


def test_launch_too_long(capsys):
    dab = DumbAutomaton(2, 3)
    ar = AutomatonRunner(5, 100)

    time_before = time()
    ar.launch(dab, dab.callback_long)
    time_after = time()
    total_time = time_after - time_before

    assert dab.rule_executed_cpt == 30  # 2 * 3 * 5
    assert dab.callback_cpt == 5
    assert total_time > 0.5  # 100 operations per seconds, we do 5. BUT each callback takes 100 ms
    assert total_time < 0.6
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 5
    assert all(s.startswith("Iteration took too long") for s in out)
