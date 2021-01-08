#!/usr/bin/python3

from automaton import automaton, automaton_runner, mpl_visualizer, neighborhood


class GameOfLife:
    LIFE = automaton.State('Life ', '#000')
    DEATH = automaton.State('Death', '#FFF')

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_death_cell(grid, x, y):
        if grid[x][y] == GameOfLife.DEATH and neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE) == 3:
            return GameOfLife.LIFE
        return grid[x][y]

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_life_cell(grid, x, y):
        alive = neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE)
        if alive == 2 or alive == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH


if __name__ == "__main__":
    ca = automaton.Automaton(10, 10)
    ca.rules = [GameOfLife.rule_death_cell, GameOfLife.rule_life_cell]
    ca.states = [GameOfLife.LIFE, GameOfLife.DEATH]

    ca.random_initialize()
    ar = automaton_runner.AutomatonRunner(10, 100)
    av = mpl_visualizer.MPLVisualizer(ca)

    ar.launch(ca, av.draw)
    av.draw(ca)
