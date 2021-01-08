"""
Command line visualizer
"""


class CLVisualizer:
    """
    CLVisualizer
    """

    def draw(self, automaton):
        states = ''
        grid = automaton.grid
        for i in range(automaton.length):
            for j in range(automaton.width):
                states += grid[i][j].name + ' '
            states += '\n'

        print(states)
