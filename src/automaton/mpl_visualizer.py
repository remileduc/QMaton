"""
Visualizer based on Matplotlib
"""

from matplotlib import pyplot as plt


class MPLVisualizer:
    """
    MPLVisualizer
    """
    def __init__(self, automaton):
        self.figure = plt.figure()
        plt.ion()
        plt.xlim(-1, automaton.width + 1)
        plt.ylim(-1, automaton.length + 1)

    def draw(self, automaton):
        class __State:
            def __init__(self, color):
                self.color = color
                self.x = []
                self.y = []

        states = {}
        grid = automaton.grid
        for i in range(automaton.length):
            for j in range(automaton.width):
                if grid[i][j].name not in states:
                    states[grid[i][j].name] = __State(grid[i][j].color)
                states[grid[i][j].name].x.append(i)
                states[grid[i][j].name].y.append(j)

        plt.clf()
        for value in states.values():
            plt.plot(value.x, value.y, 's', color=value.color)
        self.figure.canvas.draw()
