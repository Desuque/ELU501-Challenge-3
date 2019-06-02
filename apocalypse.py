from Map import *
import numpy as np
import networkx as nx

"""
# This main is the start of the Apocalypse. Here we create the first zombie population
# and we set the final day of the event
#  input : -
#  output: -
"""


def main():
    graph = nx.read_gpickle("initialGraphBis.gpickle")
    rize = None

    for cell in graph:
        if cell.rize:
            rize = cell

    zombies = {}
    # All the city turns into zombies
    totalPopulation = int(rize.population_today)
    for i in range(0, totalPopulation):
        zombies.update({Zombie(): rize})
    rize.population_today = 0
    rize.zombies = totalPopulation

    map = Map(graph, zombies)
    map.startApocalypse(100)


if __name__ == '__main__':
    main()
