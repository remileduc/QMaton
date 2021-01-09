"""
File visualizer
"""

import os
import sys


class FileVisualizer:
    """
    FileVisualizer

    Print all the steps in a file. If no file provided, write to console.
    """
    def __init__(self, file = ''):
        self._file = file
        if file and os.path.exists(file):
            os.remove(file)


    def draw(self, automaton):
        if not self._file:
            print(automaton)
            return
        with open(self._file, 'a') as f:
            f.write(str(automaton) + '\n')
