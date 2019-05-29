from Map import *
import numpy as np


def main():
    matrix = np.load("graph.npy", allow_pickle=True)

    cellZombie = matrix[81][41]  # Rize point
    zombies = []

    # All the city turns into zombies
    for i in range(0, cellZombie.population_today):
        zombies.append(Zombie(cellZombie))

    map = Map(matrix, zombies)
    map.startApocalypse(130)


if __name__ == '__main__':
    main()
