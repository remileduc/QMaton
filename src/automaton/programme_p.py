from qmaton import Automaton, neighborhood

""" ( MODELE :

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
        return GameOfLife.DEATH            )"""


""" REGLES :

- Si à la date t on avait une cellule FEU alors elle devient à la date t+1 une cellule CENDRE
- Si à la date t on avait une cellule CENDRE alors à la date t+1 elle reste une cellule CENDRE
- Si à la date t on avait une cellule VIDE alors à la date t+1 elle reste une cellule VIDE
- Si à la date t on avait une cellule ARBRE alors :
    - elle devient à la date t+1 une cellule FEU si une de ses cellule voisine est une cellule FEU
    - sinon elle reste une cellule ARBRE à la date t+1
"""

class GameOfFire:
    FEU = Automaton.State('Feu ', '#F93913')
    FEU1 = Automaton.State('Feu1 ', '#d42806')
    FEU2 = Automaton.State('Feu2 ', '#ad2003')
    FEU3 = Automaton.State('Feu3 ', '#781400')  ## expé avec temps baton seul
    CENDRE = Automaton.State('Cendre', '#676463')
    VIDE = Automaton.State('Vide', '#FFF')
    ARBRE = Automaton.State('Arbre', '#15A655')


    @staticmethod
    @neighborhood.rule_margin(1)
    def rule(grid, x, y):
        if grid[x][y] == GameOfFire.VIDE:
            return GameOfFire.rule_vide_cell(grid, x, y)
        elif grid[x][y] == GameOfFire.ARBRE:
            return GameOfFire.rule_feu_cell(grid, x, y)
        elif grid[x][y] == GameOfFire.FEU:
            return GameOfFire.rule_feu1_cell(grid, x, y)
        elif grid[x][y] == GameOfFire.FEU1:
            return GameOfFire.rule_feu2_cell(grid, x, y)
        elif grid[x][y] == GameOfFire.FEU2:
            return GameOfFire.rule_feu3_cell(grid, x, y)
        elif grid[x][y] == GameOfFire.FEU3:
            return GameOfFire.rule_cendre_cell(grid, x, y)
        return grid[x][y]

    @staticmethod
    def rule_vide_cell(grid, x, y):
        if grid[x][y] == GameOfFire.VIDE:
            return GameOfFire.VIDE
        return grid[x][y]

    @staticmethod
    def rule_feu_cell(grid, x, y):
        # Si à la date t on avait une cellule ARBRE alors elle devient à la date t+1 une cellule FEU si une de ses cellule voisine est une cellule FEU
        if grid[x][y] == GameOfFire.ARBRE and neighborhood.count_neighbors(grid, x, y, GameOfFire.FEU) >= 1:
            return GameOfFire.FEU
        return grid[x][y]

    @staticmethod
    def rule_feu1_cell(grid, x, y):
        # Si à la date t on avait une cellule FEU alors elle devient à la date t+1 une cellule FEU1 si une de ses cellule voisine est une cellule FEU
        if grid[x][y] == GameOfFire.FEU :
            return GameOfFire.FEU1
        return grid[x][y]

    @staticmethod
    def rule_feu2_cell(grid, x, y):
        # Si à la date t on avait une cellule FEU1 alors elle devient à la date t+1 une cellule FEU2 si une de ses cellule voisine est une cellule FEU
        if grid[x][y] == GameOfFire.FEU1 :
            return GameOfFire.FEU2
        return grid[x][y]

    @staticmethod
    def rule_feu3_cell(grid, x, y):
        # Si à la date t on avait une cellule FEU2 alors elle devient à la date t+1 une cellule FEU3 si une de ses cellule voisine est une cellule FEU
        if grid[x][y] == GameOfFire.FEU2 :
            return GameOfFire.FEU3
        return grid[x][y]

    @staticmethod
    def rule_cendre_cell(grid, x, y):
        if grid[x][y] == GameOfFire.FEU3:
         # Si à la date t on avait une cellule FEU3 alors elle devient à la date t+1 une cellule CENDRE
            return GameOfFire.CENDRE
        return grid[x][y]


    @staticmethod
    def get_automaton(width, length):
        """Create an Automaton, already set up with rules and states.

        :param int width: the width of the grid of the automaton
        :param int length: the length of the grid of the automaton
        :return Automaton: an automaton with states and rules
        """
        ca = Automaton(width, length, GameOfFire.VIDE)
        ca.states = [GameOfFire.FEU, GameOfFire.CENDRE, GameOfFire.VIDE, GameOfFire.ARBRE]
        ca.rule = GameOfFire.rule
        return ca


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from visualizer import QtVisualizer

    app = QApplication([])

    ca = GameOfFire.get_automaton(30, 30)

    # Initialize
    ca.random_initialize()

    av = QtVisualizer(ca)

    av.show()
    app.exec_()
