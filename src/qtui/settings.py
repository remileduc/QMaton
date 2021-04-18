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

"""Settings for the QMaton MainWindow class.

Settings are saved in an .ini file
"""

import json

from PyQt5.QtCore import QByteArray, QSettings
from qmaton import AutomatonSerializer

organization = "remileduc"
"""The organization used to store the settings."""

application = "QMaton"
"""The application name."""

save_path = ""
"""The last path used to open / save file."""


def save_settings(main_window):
    settings = __get_settings(main_window)
    settings.setValue("ips", main_window.spIPS.value())
    settings.setValue("nbSteps", main_window.spNbSteps.value())
    global save_path
    settings.setValue("save_path", save_path)

    settings.beginGroup("automaton")
    settings.setValue("dump", json.dumps(main_window._automaton, cls=AutomatonSerializer))
    settings.endGroup()

    settings.beginGroup("window")
    settings.setValue("geometry", main_window.saveGeometry())
    settings.setValue("state", main_window.saveState())
    settings.endGroup


def restore_settings(main_window):
    settings = __get_settings(main_window)
    main_window.spIPS.setValue(settings.value("ips", 10, type=int))
    main_window.spNbSteps.setValue(settings.value("nbSteps", -1, type=int))
    global save_path
    save_path = settings.value("save_path", "", type=str)

    if settings.contains("automaton/dump"):
        main_window.set_automaton(main_window._automaton_type.fromJSON(settings.value("automaton/dump", type=str)))

    settings.beginGroup("window")
    main_window.restoreGeometry(settings.value("geometry", type=QByteArray))
    main_window.restoreState(settings.value("state", type=QByteArray))
    settings.endGroup


def __get_settings(parent=None):
    global organization
    global application
    return QSettings(QSettings.IniFormat, QSettings.UserScope, organization, application, parent)
