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
from qmaton import Automaton, AutomatonHistory, AutomatonRunner
from qtui import resources, settings  # noqa: F401


class MainWindow(QMainWindow):
    """Main window for QMaton UI.

    This is using the MainWindow.ui file. Note that most of the Qt connections are done in the UI file.
    """

    def __init__(self, automaton_type, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "MainWindow.ui"), self)
        self._history = AutomatonHistory()
        self._automaton = None
        self._automaton_type = automaton_type
        self.__is_running = False

        # set media buttons
        self.btnPlay.setDefaultAction(self.actionPlayPause)
        self.btnBack.setDefaultAction(self.actionBack)
        self.btnForward.setDefaultAction(self.actionForward)

        # restore preferences
        settings.restore_settings(self)

    def set_automaton(self, automaton):
        self._automaton = automaton
        self._automaton_type = type(automaton)
        self.wautomaton.set_automaton(self._automaton)
        self.__clear_history()
        self.spLength.setValue(self._automaton.length)
        self.spWidth.setValue(self._automaton.width)

    # Automaton slots

    @pyqtSlot()
    def _automaton_started(self):
        self.__is_running = True
        self.__enable_ui(False)
        self.actionPlayPause.setIcon(QIcon(":/media/pause"))

    @pyqtSlot()
    def _automaton_finished(self):
        self.__is_running = False
        self.__enable_ui(True)
        self.actionPlayPause.setIcon(QIcon(":/media/play"))

    @pyqtSlot(Automaton)
    def _automaton_step_calculated(self, automaton):
        self.__updateSlider()

    # Menu slots

    @pyqtSlot()
    def _open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select open file", settings.save_path, "JSON Automaton (*.json)"
        )
        if not filename:
            return
        with open(filename, "r") as file:
            self.set_automaton(self._automaton_type.fromJSON(file.read()))
        settings.save_path = filename

    @pyqtSlot()
    def _save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Select save file", settings.save_path, "JSON Automaton (*.json)"
        )
        if not filename:
            return
        with open(filename, "w") as file:
            file.write(self._automaton.toJSON())
        settings.save_path = filename

    @pyqtSlot()
    def _reset_grid(self):
        self._automaton_started()
        self._automaton.grid = self._history.move_to(0)
        self.__clear_history()
        self.__draw_automaton()

    @pyqtSlot()
    def _randomize_grid(self):
        self._automaton_started()
        self._automaton.random_initialize()
        self.__clear_history()
        self.__draw_automaton()

    @pyqtSlot()
    def _clear_grid(self):
        self._automaton_started()
        self._automaton.clear_grid()
        self.__clear_history()
        self.__draw_automaton()

    # Media slots

    @pyqtSlot()
    def _start_pause_automaton(self):
        if self.__is_running:
            self.wautomaton.stop()
        else:
            self._automaton_started()
            self.wautomaton.run(AutomatonRunner(10, self.spIPS.value(), history=self._history))

    @pyqtSlot()
    def _run_backward(self):
        if self._history.current_index > 0:
            self._automaton_started()
            self._automaton.grid = self._history.move_backward()
            self.__updateSlider()
            self.__draw_automaton()

    @pyqtSlot()
    def _run_forward(self):
        self._automaton_started()
        if not self._history.remaining_steps:
            self.wautomaton.run_seq(AutomatonRunner(1, history=self._history))
        else:
            self._automaton.grid = self._history.move_forward()
            self.__updateSlider()
            self.__draw_automaton()

    @pyqtSlot(int)
    def _set_step(self, step):
        self._automaton_started()
        self._automaton.grid = self._history.move_to(step)
        self.__updateSlider()
        self.__draw_automaton()

    # Settings slots

    @pyqtSlot()
    def _settings_validated(self):
        length = self.spLength.value()
        width = self.spWidth.value()
        if self._automaton.grid_size != (length, width):
            self.set_automaton(self._automaton_type(length, width))

    # Override

    def closeEvent(self, event):
        settings.save_settings(self)
        super().closeEvent(event)

    # Private methods

    def __draw_automaton(self):
        self._automaton_started()
        self.wautomaton.draw()
        self._automaton_finished()

    def __clear_history(self):
        self._history.clear()
        self.__updateSlider()

    def __enable_ui(self, enabled):
        # actions file
        self.actionOpen.setEnabled(enabled)
        self.actionSave.setEnabled(enabled)
        # actions edit
        self.actionReset.setEnabled(self._history.current_index > 0 if enabled else False)
        self.actionRandomizeGrid.setEnabled(enabled)
        self.actionClear.setEnabled(enabled)
        # settings
        self.settingsWidget.setEnabled(enabled)
        # media buttons
        self.actionForward.setEnabled(enabled)
        self.actionBack.setEnabled(self._history.current_index > 0 if enabled else False)
        self.timeSlider.setEnabled(enabled)

    def __updateSlider(self):
        timemax = max(0, len(self._history) - 1)
        tumecur = max(0, self._history.current_index)

        self.timeSlider.blockSignals(True)
        self.timeSlider.setMaximum(timemax)
        self.timeSlider.setValue(tumecur)
        self.timeSlider.blockSignals(False)
        self.lblTime.setText(f"({tumecur} / {timemax}) ")
