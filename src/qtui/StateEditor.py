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

"""State editor widget for QMaton UI."""

from PyQt5.QtCore import QPoint, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QWidget
from qmaton import Automaton, State
from visualizer import QtVisualizer


class StateEditor(QWidget):
    """State editor widget for QMaton UI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__wautomaton: QtVisualizer = None
        self.__states: list[State] = []
        self.__current_state: State = None
        self.__layout = QBoxLayout(QBoxLayout.TopToBottom, self)

    def visualizer(self) -> QtVisualizer:
        return self.__wautomaton

    # Slots

    @pyqtSlot(QtVisualizer)
    def set_visualizer(self, visualizer: QtVisualizer) -> None:
        self.__wautomaton = visualizer
        self.__wautomaton.automaton_has_changed.connect(self.__update_states)
        self.__wautomaton.cell_clicked.connect(self.__cell_clicked)
        if self.__wautomaton._automaton:
            self.__update_states(self.__wautomaton._automaton)

    # Override

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__layout.setDirection(
            QBoxLayout.TopToBottom if event.size().height() > event.size().width() else QBoxLayout.LeftToRight
        )
        super().resizeEvent(event)

    # Private slots

    @pyqtSlot(Automaton)
    def __update_states(self, automaton: Automaton) -> None:
        if automaton.states == self.__states:
            return
        self.__states = automaton.states
        self.__current_state = None
        self.__clear_layout()
        self.__fill_layout()

    @pyqtSlot(QPoint)
    def __cell_clicked(self, pos: QPoint) -> None:
        if self.__current_state:
            self.__wautomaton.set_cell_state(pos, self.__current_state)

    @pyqtSlot(bool)
    def __btn_toggled(self, checked: bool, state: State):
        btn = self.sender()
        if not btn:
            return
        self.__blockSignals(True)
        if not checked:  # go back to none
            self.__current_state = None
            self.__layout.itemAt(0).widget().setChecked(True)
        else:  # unselect any previously selected btn
            self.__current_state = state
            for i in range(self.__layout.count()):
                widget = self.__layout.itemAt(i).widget()
                if widget and widget is not btn:
                    widget.setChecked(False)
        self.__blockSignals(False)

    # Private methods

    def __clear_layout(self) -> None:
        while self.__layout.count():
            item = self.__layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def __fill_layout(self) -> None:
        state = None
        btn = QPushButton(QIcon(":/icons/cancel"), "None", self)
        btn.setCheckable(True)
        btn.toggled.connect(lambda checked, state=state, self=self: self.__btn_toggled(checked, state))
        self.__layout.addWidget(btn)
        for state in self.__states:
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(state.color))
            btn = QPushButton(QIcon(pixmap), state.name, self)
            btn.setCheckable(True)
            btn.toggled.connect(lambda checked, state=state, self=self: self.__btn_toggled(checked, state))
            self.__layout.addWidget(btn)
        self.__layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

    def __blockSignals(self, block: bool) -> None:
        self.blockSignals(block)
        for i in range(self.__layout.count()):
            widget = self.__layout.itemAt(i).widget()
            if widget:
                widget.blockSignals(block)
