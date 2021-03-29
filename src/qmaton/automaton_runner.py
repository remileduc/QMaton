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

"""Automaton runner."""


from time import sleep, time


class AutomatonRunner:
    """AutomatonRunner

    Run iterations on the Automaton as many times as desired. It call the
    method `Automaton.apply_rule()`.

    Attributes:
        sleep_time the number of ms between each iteration
        nb_iter the number of iterations to do
        history the history manager to update
    """

    def __init__(self, nb_iter=100, iter_per_second=10, history=None):
        """Constructor

        :param int nb_iter: the number of iterations to realize
        :param float iter_per_second: number of iterations per second (can't be 0)
        """
        self.sleep_time = 1 / iter_per_second
        self.nb_iter = nb_iter
        self.history = history
        self.__stop = False

    def stop(self):
        """Stop the runner."""
        self.__stop = True

    def launch(self, automaton, callback=None):
        """Start the runner.

        The time this function will run should be nb_iter * sleep_time seconds
        (or nb_iter / iter_per_second seconds).

        Note that this function should be ran in a separate thread to avoid any freeze.

        :param Automaton automaton: the automaton to run on
        :param Callable callback: a callable object called each time an iteration is finished
        """
        self.__stop = False
        i = 0
        while not self.__stop and i < self.nb_iter:
            time_before = time()
            if self.history is not None and not self.history:  # history is empty
                self.history.append_automaton_state(automaton)

            automaton.apply_rule()
            if self.history is not None:
                self.history.append_automaton_state(automaton)
            if callback is not None:
                callback(automaton)

            to_sleep = self.sleep_time - time() + time_before
            if to_sleep > 0:
                sleep(self.sleep_time)
            else:
                print("Iteration took too long: {} s".format(self.sleep_time - to_sleep))
            i += 1
