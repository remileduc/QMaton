from automaton import automaton

class GameOfLife:
    LIFE = automaton.State('Life ', '#000')
    DEATH = automaton.State('Death', '#FFF')

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_death_cell(grid, x, y):
        if grid[x][y] == GameOfLife.DEATH and neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE) == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH

    @staticmethod
    @neighborhood.rule_margin(1)
    def rule_life_cell(grid, x, y):
        alive = neighborhood.count_neighbors(grid, x, y, GameOfLife.LIFE)
        if alive == 2 or alive == 3:
            return GameOfLife.LIFE
        return GameOfLife.DEATH