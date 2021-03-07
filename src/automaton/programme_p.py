from qmaton import Automaton, State, VonNeumannNeighborhood

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


class GameOfFire(Automaton):
    FEU = State("Feu ", "#F93913")
    FEU1 = State("Feu1 ", "#d42806")
    FEU2 = State("Feu2 ", "#ad2003")
    FEU3 = State("Feu3 ", "#781400")  # expé avec temps baton seul
    CENDRE = State("Cendre", "#676463")
    VIDE = State("Vide", "#FFF")
    ARBRE = State("Arbre", "#15A655")

    FIRE_LIST = (FEU, FEU1, FEU2, FEU3)

    def __init__(self, length=10, width=10):
        super().__init__(length, width, GameOfFire.VIDE)
        self.states = [
            GameOfFire.FEU,
            GameOfFire.FEU1,
            GameOfFire.FEU2,
            GameOfFire.FEU3,
            GameOfFire.CENDRE,
            GameOfFire.VIDE,
            GameOfFire.ARBRE,
        ]
        self.rule = self.main_rule
        self.neighborhood = VonNeumannNeighborhood()

    def main_rule(self, x, y):
        if self.grid[x][y] == GameOfFire.VIDE:
            return self.rule_vide_cell(x, y)
        elif self.grid[x][y] == GameOfFire.ARBRE:
            return self.rule_feu_cell(x, y)
        elif self.grid[x][y] == GameOfFire.FEU:
            return self.rule_feu1_cell(x, y)
        elif self.grid[x][y] == GameOfFire.FEU1:
            return self.rule_feu2_cell(x, y)
        elif self.grid[x][y] == GameOfFire.FEU2:
            return self.rule_feu3_cell(x, y)
        elif self.grid[x][y] == GameOfFire.FEU3:
            return self.rule_cendre_cell(x, y)
        return self.grid[x][y]

    def rule_vide_cell(self, x, y):
        if self.grid[x][y] == GameOfFire.VIDE:
            return GameOfFire.VIDE
        return self.grid[x][y]

    def rule_feu_cell(self, x, y):
        # Si à la date t on avait une cellule ARBRE alors elle devient à la date t+1 une cellule FEU
        # si une de ses cellule voisine est une cellule FEU
        if (
            self.grid[x][y] == GameOfFire.ARBRE
            and self.count_neighbors(self.neighborhood, x, y, GameOfFire.FIRE_LIST) >= 1
        ):
            return GameOfFire.FEU
        return self.grid[x][y]

    def rule_feu1_cell(self, x, y):
        # Si à la date t on avait une cellule FEU alors elle devient à la date t+1 une cellule FEU1
        # si une de ses cellule voisine est une cellule FEU
        if self.grid[x][y] == GameOfFire.FEU:
            return GameOfFire.FEU1
        return self.grid[x][y]

    def rule_feu2_cell(self, x, y):
        # Si à la date t on avait une cellule FEU1 alors elle devient à la date t+1 une cellule
        # FEU2 si une de ses cellule voisine est une cellule FEU
        if self.grid[x][y] == GameOfFire.FEU1:
            return GameOfFire.FEU2
        return self.grid[x][y]

    def rule_feu3_cell(self, x, y):
        # Si à la date t on avait une cellule FEU2 alors elle devient à la date t+1 une cellule
        # FEU3 si une de ses cellule voisine est une cellule FEU
        if self.grid[x][y] == GameOfFire.FEU2:
            return GameOfFire.FEU3
        return self.grid[x][y]

    def rule_cendre_cell(self, x, y):
        # Si à la date t on avait une cellule FEU3 alors elle devient à la date t+1 une cellule CENDRE
        if self.grid[x][y] == GameOfFire.FEU3:
            return GameOfFire.CENDRE
        return self.grid[x][y]


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from visualizer import QtVisualizer

    app = QApplication([])

    ca = GameOfFire(30, 30)

    # Initialize
    ca.random_initialize()

    av = QtVisualizer(ca)

    av.show()
    app.exec_()
