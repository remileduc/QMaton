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

"""Test file for QtVisualizer and QtVisualizerWorker classes"""

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from pytest import fixture
from qmaton import Automaton, AutomatonHistory, AutomatonRunner, State
from visualizer.qt_visualizer import QtVisualizer, QtVisualizerWorker


class DumbAutomaton(Automaton):
    STATE = State("state", "#000")

    def __init__(self, width, length):
        super().__init__(width, length, DumbAutomaton.STATE)
        self.states = [DumbAutomaton.STATE]
        self.rule = self.main_rule

    def main_rule(self, x, y):
        return self.grid[x][y]


class SignalCounter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.started_count = 0
        self.step_count = 0
        self.finished_count = 0

    def connect(self, o):
        o.started.connect(self.started)
        o.step_calculated.connect(self.stepped)
        o.finished.connect(self.finished)

    @pyqtSlot()
    def started(self):
        self.started_count += 1

    @pyqtSlot(Automaton)
    def stepped(self, _):
        self.step_count += 1

    @pyqtSlot()
    def finished(self):
        self.finished_count += 1


@fixture()
def app():
    return QApplication([])


# QtVisualizerWorker


def test_QtVisualizerWorker_init():
    automaton = ["automaton"]
    automaton_runner = ["AutomatonRunner"]
    w = QtVisualizerWorker(automaton, automaton_runner)
    assert w._automaton is automaton
    assert w._automatonRunner is automaton_runner


def test_QtVisualizerWorker_run():
    w = QtVisualizerWorker(DumbAutomaton(5, 5), AutomatonRunner(10, 1000))
    s = SignalCounter()
    s.connect(w)
    w.run()
    assert s.started_count == 1
    assert s.step_count == 10
    assert s.finished_count == 1


# QtVisualizer


def test_QtVisualizer_init(app):
    qv = QtVisualizer()
    assert qv._automaton is None


def test_QtVisualizer_set_automaton(app):
    qv = QtVisualizer()
    s = SignalCounter()
    s.connect(qv)
    qv.set_automaton(DumbAutomaton(5, 5))
    assert s.started_count == 1
    assert s.step_count == 0
    assert s.finished_count == 1
    qv.set_automaton(DumbAutomaton(5, 5))
    assert s.started_count == 2
    assert s.step_count == 0
    assert s.finished_count == 2


def test_QtVisualizer_run_seq(app):
    qv = QtVisualizer()
    qv.set_automaton(DumbAutomaton(5, 5))
    s = SignalCounter()
    s.connect(qv)
    qv.run_seq(AutomatonRunner(10, 1000))
    assert s.started_count == 1
    assert s.step_count == 10
    assert s.finished_count == 1


def test_QtVisualizer_run(app):
    qv = QtVisualizer()
    qv.set_automaton(DumbAutomaton(5, 5))
    hist = AutomatonHistory()
    t = qv.run(AutomatonRunner(10, 1000, hist))
    assert t.isRunning()
    t.wait(500)
