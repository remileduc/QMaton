#!/usr/bin/python3

from automaton import automaton, automaton_runner, file_visualizer, neighborhood


if __name__ == "__main__":
    ca = automaton.Automaton(10, 10)
    ca.rules = [GameOfLife.rule_death_cell, GameOfLife.rule_life_cell]
    ca.states = [GameOfLife.LIFE, GameOfLife.DEATH]

    ca.random_initialize()
    ar = automaton_runner.AutomatonRunner(10, 100)
    #av = file_visualizer.FileVisualizer("test.txt")
    av = file_visualizer.FileVisualizer()

    ar.launch(ca, av.draw)
    av.draw(ca)
