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

"""Show the automaton in a UI window."""


from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QMenu, QWidget
from qmaton import Automaton, AutomatonRunner


class QtVisualizerWorker(QObject):
    """Worker for QtVisualizer."""

    started = pyqtSignal()
    finished = pyqtSignal()
    step_calculated = pyqtSignal(Automaton)

    def __init__(self, automaton, automatonRunner, parent=None):
        super().__init__(parent)
        self._automaton = automaton
        self._automatonRunner = automatonRunner

    @pyqtSlot()
    def run(self):
        self.started.emit()
        self._automatonRunner.launch(self._automaton, lambda automaton: self.step_calculated.emit(automaton))
        self.finished.emit()


class QtVisualizer(QWidget):
    """Show the automaton in a UI window."""

    started = pyqtSignal()
    finished = pyqtSignal()
    step_calculated = pyqtSignal(Automaton)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = None
        self._worker = None
        self._automaton = None
        self.__layout = QGridLayout(self)

    def set_automaton(self, automaton):
        self._automaton = automaton
        self.__clearLayout()

        label = None
        for line in range(self._automaton.length):
            for cell in range(self._automaton.width):
                label = QLabel(self)
                label.setContextMenuPolicy(Qt.CustomContextMenu)
                label.customContextMenuRequested.connect(
                    lambda pos, lbl=label, x=line, y=cell: self.__label_contextual_menu(lbl.mapToGlobal(pos), x, y)
                )
                self.__layout.addWidget(label, line, cell)
        self.draw()

    @pyqtSlot(Automaton)
    def draw(self, automaton=None):
        """Callback for the AutomatonRunner."""
        if not automaton:
            automaton = self._automaton
        grid = automaton.grid
        for i in range(automaton.length):
            for j in range(automaton.width):
                self.__change_label_color(i, j, grid[i][j].color)

    @pyqtSlot(AutomatonRunner)
    def run(self, automatonRunner):
        self.__initialize_worker(automatonRunner)
        # Start thread
        self._thread.start()

    @pyqtSlot()
    def stop(self):
        self._thread.exit(-1)

    def __clearLayout(self):
        while self.__layout.count():
            item = self.__layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def __initialize_worker(self, automatonRunner):
        # Create thread environment
        self._thread = QThread(self)
        self._worker = QtVisualizerWorker(self._automaton, automatonRunner)
        self._worker.moveToThread(self._thread)
        # Connect everything
        self._thread.started.connect(self._worker.run)
        self._worker.started.connect(self.started)
        self._worker.finished.connect(self.finished)
        self._worker.step_calculated.connect(self.step_calculated)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.step_calculated.connect(self.draw)

    def __label_contextual_menu(self, pos, x, y):
        if self._thread and self._thread.isRunning():
            return

        state = None
        oldState = self._automaton.grid[x][y]

        def __set_state(newState):
            nonlocal state
            state = newState

        # create menu
        menu = QMenu(self)
        for s in self._automaton.states:
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(s.color))
            action = menu.addAction(QIcon(pixmap), s.name)
            action.triggered.connect(lambda _, newState=s: __set_state(newState))
            if s == oldState:
                font = action.font()
                font.setBold(True)
                action.setFont(font)
        # show menu
        menu.exec(pos)
        # change state if a new one has been selected
        if state is not None and state != oldState:
            self._automaton.grid[x][y] = state
            self.__change_label_color(x, y, state.color)

    def __change_label_color(self, x, y, color):
        self.__layout.itemAtPosition(x, y).widget().setStyleSheet(f"QLabel {{ background-color : {color} }}")
