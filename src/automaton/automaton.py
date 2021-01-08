"""Automaton"""

import random
from collections import namedtuple
from copy import deepcopy


State = namedtuple('State', ['name', 'color'])


class Automaton:
    """"Automaton"""

    def __init__(self, width=10, length=10):
        self.width = width
        self.length = length
        self.states = []
        self.rules = []
        self.grid = [[None for _ in range(width)] for _ in range(length)]

    def __str__(self):
        s = ''
        for line in self.grid:
            for cell in line:
                s += cell.name + ' '
            s += '\n'
        return s

    def random_initialize(self):
        if not self.states:
            self.grid = [[None for _ in range(self.width)]
                         for _ in range(self.length)]
        else:
            random.seed()
            self.grid = [[self.states[random.randrange(len(self.states))]
                          for _ in range(self.width)] for _ in range(self.length)]

    def apply_rules(self):
        new_grid = deepcopy(self.grid)
        # apply rules for each cell
        for i in range(self.length):
            for j in range(self.width):
                for rule in self.rules:
                    new_grid[i][j] = rule(new_grid, i, j)
                    # if rule matched, skip the others
                    if self.grid[i][j] != new_grid[i][j]:
                        break
        self.grid = new_grid
