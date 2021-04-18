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

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QProgressBar
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
        self.__statusprogress = None
        self.__lastmax = 0
        self.__statuslabel = QLabel(self)
        self.statusbar.addPermanentWidget(self.__statuslabel)

        # set media buttons
        self.btnPlay.setDefaultAction(self.actionPlayPause)
        self.btnBack.setDefaultAction(self.actionBack)
        self.btnForward.setDefaultAction(self.actionForward)

        # set dock actions
        action = self.dockSettings.toggleViewAction()
        action.setIcon(QIcon(":/icons/settings"))
        self.menuView.addAction(action)
        action = self.dockEditor.toggleViewAction()
        action.setIcon(QIcon(":/icons/edit"))
        self.menuView.addAction(action)

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
        self.statusbar.showMessage("Running Automaton...")

    @pyqtSlot()
    def _automaton_finished(self):
        self.__is_running = False
        self.__enable_ui(True)
        self.actionPlayPause.setIcon(QIcon(":/media/play"))
        self.statusbar.clearMessage()
        if self.__statusprogress:
            self.statusbar.removeWidget(self.__statusprogress)
            self.__statusprogress.deleteLater()
            self.__statusprogress = None

    @pyqtSlot(Automaton)
    def _automaton_step_calculated(self, automaton):
        self.__update_slider()

    @pyqtSlot()
    def _automaton_grid_changed(self):
        self.__clear_history()
        self.statusbar.showMessage("Grid has changed", 2500)

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
        self.statusbar.showMessage(f"File open: '{filename}'", 2500)

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
        self.statusbar.showMessage(f"Saved to file: '{filename}'", 2500)

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
            self.wautomaton.run(AutomatonRunner(self.spNbSteps.value(), self.spIPS.value(), history=self._history))
            if self.spNbSteps.value() > 0:
                self.__create_progressbar()

    @pyqtSlot()
    def _run_backward(self):
        if self._history.current_index > 0:
            self._automaton_started()
            self._automaton.grid = self._history.move_backward()
            self.__update_slider()
            self.__draw_automaton()

    @pyqtSlot()
    def _run_forward(self):
        self._automaton_started()
        if not self._history.remaining_steps:
            self.wautomaton.run_seq(AutomatonRunner(1, history=self._history))
        else:
            self._automaton.grid = self._history.move_forward()
            self.__update_slider()
            self.__draw_automaton()

    @pyqtSlot(int)
    def _set_step(self, step):
        self._automaton_started()
        self._automaton.grid = self._history.move_to(step)
        self.__update_slider()
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
        self.__update_slider()

    def __enable_ui(self, enabled):
        # actions file
        self.actionOpen.setEnabled(enabled)
        self.actionSave.setEnabled(enabled)
        # actions edit
        self.actionReset.setEnabled(self._history.current_index > 0 if enabled else False)
        self.actionRandomizeGrid.setEnabled(enabled)
        self.actionClear.setEnabled(enabled)
        # settings
        self.dockSettings.setEnabled(enabled)
        self.dockEditor.setEnabled(enabled)
        # media buttons
        self.actionForward.setEnabled(enabled)
        self.actionBack.setEnabled(self._history.current_index > 0 if enabled else False)
        self.timeSlider.setEnabled(enabled)

    def __update_slider(self):
        timemax = max(0, len(self._history) - 1)
        timecur = max(0, self._history.current_index)

        self.timeSlider.blockSignals(True)
        self.timeSlider.setMaximum(timemax)
        self.timeSlider.setValue(timecur)
        self.timeSlider.blockSignals(False)
        self.lblTime.setText(f"({timecur} / {timemax}) ")
        self.__statuslabel.setText(f"Step {timecur} over {timemax}")
        if self.__statusprogress:
            self.__statusprogress.setValue(timecur - self.__lastmax)

    def __create_progressbar(self):
        self.__statusprogress = QProgressBar(self)
        self.__statusprogress.setAlignment(Qt.AlignHCenter)
        self.__statusprogress.setMaximum(self.spNbSteps.value())
        self.__statusprogress.setValue(0)
        self.__statusprogress.setFormat("%v / %m")
        self.__lastmax = max(0, self._history.current_index)
        self.statusbar.insertPermanentWidget(0, self.__statusprogress)
