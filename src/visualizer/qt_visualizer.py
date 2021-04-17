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


from PyQt5.QtCore import QObject, QPoint, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QMenu, QWidget
from qmaton import Automaton, AutomatonRunner


class QtVisualizerWorker(QObject):
    """Worker for QtVisualizer."""

    started = pyqtSignal()
    finished = pyqtSignal()
    step_calculated = pyqtSignal(Automaton)

    def __init__(self, automaton: Automaton, automatonRunner: AutomatonRunner, parent: QObject = None):
        super().__init__(parent)
        self._automaton: Automaton = automaton
        self._automatonRunner: AutomatonRunner = automatonRunner

    @pyqtSlot()
    def run(self) -> None:
        self.started.emit()
        self._automatonRunner.launch(self._automaton, lambda automaton: self.step_calculated.emit(automaton))
        self.finished.emit()


class QtVisualizer(QWidget):
    """Show the automaton in a UI window."""

    started = pyqtSignal()
    """Emitted when we start running the automaton, or when we change the automaton."""
    finished = pyqtSignal()
    """Emitted when the running or the change of automaton is finished."""
    step_calculated = pyqtSignal(Automaton)
    """Emitted during automaton running, at each step."""
    grid_changed = pyqtSignal()
    """Emitted when th grid is editted."""
    automaton_has_changed = pyqtSignal(Automaton)
    """Emitted when the automaton has changed (possible change of states)."""
    cell_clicked = pyqtSignal(QPoint)
    """Emitted when a cell has been clicked."""

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._thread: QThread = None
        self._worker: QtVisualizerWorker = None
        self._automaton: Automaton = None
        self.__automaton_runner: AutomatonRunner = None
        self.__layout: QGridLayout = QGridLayout(self)
        self.__layout.setSpacing(1)
        self.__is_running: bool = False

    def set_automaton(self, automaton: Automaton) -> None:
        """Reset the widget to show the given automaton.

        In case the automaton is the same but you just want to update the widget, you should call the draw()
        method instead.
        """
        self.__start()
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
        self.__stop()
        self.automaton_has_changed.emit(self._automaton)

    def is_running(self) -> bool:
        """Tells if we are currently running the automaton."""
        return self.__is_running

    # Slots

    @pyqtSlot(Automaton)
    def draw(self, automaton: Automaton = None) -> None:
        """Callback for the AutomatonRunner."""
        if not automaton:
            automaton = self._automaton
        grid = automaton.grid
        for i in range(automaton.length):
            for j in range(automaton.width):
                self.__change_label_color(i, j, grid[i][j].color)

    @pyqtSlot(AutomatonRunner)
    def run(self, automatonRunner: AutomatonRunner) -> QThread:
        """Run the automaton through the given AutomatonRunner in a separate thread."""
        self.__initialize_worker(automatonRunner)
        self.__initialize_thread()
        # Start thread
        self._thread.start()
        return self._thread

    @pyqtSlot(AutomatonRunner)
    def run_seq(self, automatonRunner: AutomatonRunner) -> None:
        """Run the automaton through the given AutomatonRunner in the current thread (sequentially)."""
        self.__initialize_worker(automatonRunner)
        # Start runner
        self._worker.run()

    @pyqtSlot()
    def stop(self) -> None:
        if self.__automaton_runner:
            self.__automaton_runner.stop()
        if self._thread and self._thread.isRunning():
            self._thread.exit(-1)

    # Override

    def mouseReleaseEvent(self, event):
        if self.is_running():
            return
        w = self.childAt(event.pos())
        if not w or not isinstance(w, QLabel):
            return
        # try to find the position of the label
        for i in range(self.__layout.count()):
            if self.__layout.itemAt(i).widget() is w:
                (x, y, _, _) = self.__layout.getItemPosition(i)
                self.cell_clicked.emit(QPoint(x, y))
                return

    # Private methods

    def __clearLayout(self) -> None:
        while self.__layout.count():
            item = self.__layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def __initialize_worker(self, automatonRunner: AutomatonRunner) -> None:
        self.__automaton_runner = automatonRunner
        # Create thread environment
        self._worker = QtVisualizerWorker(self._automaton, automatonRunner)
        # Connect everything
        self._worker.started.connect(self.__start)
        self._worker.finished.connect(self.__stop)
        self._worker.step_calculated.connect(self.step_calculated)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.step_calculated.connect(self.draw)

    def __initialize_thread(self) -> None:
        # Create thread environment
        self._thread = QThread(self)
        self._worker.moveToThread(self._thread)
        # Connect everything
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._thread.quit, Qt.DirectConnection)

    def __label_contextual_menu(self, pos: QPoint, x: int, y: int) -> None:
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
            self.grid_changed.emit()

    def __change_label_color(self, x: int, y: int, color: str):
        self.__layout.itemAtPosition(x, y).widget().setStyleSheet(f"QLabel {{ background-color : {color} }}")

    # Private slots

    @pyqtSlot()
    def __start(self):
        self.__is_running = True
        self.started.emit()

    @pyqtSlot()
    def __stop(self):
        self.__is_running = False
        self.finished.emit()
