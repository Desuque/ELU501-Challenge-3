from Map import *
import numpy as np
import networkx as nx


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
    map.startApocalypse(1)


if __name__ == '__main__':
    main()
