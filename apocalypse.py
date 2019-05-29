from Map import *
import numpy as np


def main():
    matrix = np.load("graph.npy", allow_pickle=True)

    cellZombie = matrix[131][276]  # Rize point
    zombies = []

    # All the city turns into zombies
    for i in range(0, int(cellZombie.population_today)):
        zombies.append(Zombie(cellZombie))
        cellZombie.population_today = 0

    map = Map(matrix, zombies)
    map.startApocalypse(130)


if __name__ == '__main__':
    main()
