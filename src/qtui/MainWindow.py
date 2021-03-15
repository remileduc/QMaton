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

"""Main Window entry for QMaton UI."""

from os import path

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from qmaton import Automaton, AutomatonRunner
from qtui import resources  # noqa: F401


class MainWindow(QMainWindow):
    """Main window for QMaton UI.

    This is using the MainWindow.ui file. Note that most of the Qt connections are done in the UI file.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "MainWindow.ui"), self)
        self._automaton = None
        self.__is_running = False

    def set_automaton(self, automaton):
        self._automaton = automaton
        self.wautomaton.set_automaton(self._automaton)

    # Automaton slots

    @pyqtSlot()
    def _automaton_started(self):
        self.__is_running = True
        self.__enable_ui(False)

    @pyqtSlot()
    def _automaton_finished(self):
        self.__is_running = False
        self.__enable_ui(True)
        self.btnPlay.setIcon(QIcon(":/media/play"))

    @pyqtSlot(Automaton)
    def _automaton_step_calculated(self, automaton):
        pass

    # Menu slots

    @pyqtSlot()
    def _open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select open file", "automaton", "JSON Automaton (*.json)")
        if not filename:
            return
        with open(filename, "r") as file:
            self.set_automaton(type(self._automaton).fromJSON(file.read()))

    @pyqtSlot()
    def _save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Select save file", "automaton", "JSON Automaton (*.json)")
        if not filename:
            return
        with open(filename, "w") as file:
            file.write(self._automaton.toJSON())

    @pyqtSlot()
    def _reset_grid(self):
        pass

    @pyqtSlot()
    def _randomize_grid(self):
        if not self._automaton:
            return
        self._automaton.random_initialize()
        self.__draw_automaton()

    @pyqtSlot()
    def _clear_grid(self):
        if not self._automaton:
            return
        self._automaton.clear_grid()
        self.__draw_automaton()

    # Media slots

    @pyqtSlot()
    def _start_pause_automaton(self):
        if not self.__is_running:
            self.__is_running = True
            self.btnPlay.setIcon(QIcon(":/media/pause"))
            self.wautomaton.run(AutomatonRunner(10, 10))
        else:
            self.wautomaton.stop()

    @pyqtSlot()
    def _run_forward(self):
        if self.__is_running:
            return
        self._automaton_started()
        self._automaton.apply_rule()
        self.__draw_automaton()

    def __draw_automaton(self):
        self._automaton_started()
        self.wautomaton.draw()
        self._automaton_step_calculated(self._automaton)
        self._automaton_finished()

    def __enable_ui(self, enabled):
        # actions file
        self.actionOpen.setEnabled(enabled)
        self.actionSave.setEnabled(enabled)
        # actions edit
        self.actionReset.setEnabled(enabled)
        self.actionRandomizeGrid.setEnabled(enabled)
        self.actionClear.setEnabled(enabled)
        # settings
        self.settingsWidget.setEnabled(enabled)
        # media buttons
        self.btnBack.setEnabled(enabled)
        self.btnForward.setEnabled(enabled)
