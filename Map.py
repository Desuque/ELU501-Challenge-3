import matplotlib.pyplot as plt
import numpy as np


class Cell(object):
    def __init__(self, elevation, population):
        self.elevation = elevation
        self.population_today = population

        # Only for the images
        self.zombies = 0


class Zombie(object):
    def __init__(self, cell=None):
        self.zombieDays = 0
        self.cell = cell
        self.arrived = False


class Map(object):

    def __init__(self, map, zombies):
        self.map = map
        self.initX = None
        self.initY = None
        self.actualJour = 0
        self.zombies = zombies
        self.number_image = 0

    def getTotalTodayPopulation(self, neighbors):
        total_population = 0
        for neighbor in neighbors:
            total_population += neighbor.population_today

        return total_population

    def moveZombies(self, cellOrigin, cellDest, numberToMove):
        zombiesPassed = 0
        for zombie in self.zombies:
            if zombie.cell == cellOrigin and zombiesPassed < numberToMove and not zombie.arrived:
                zombie.cell = cellDest
                zombiesPassed += 1
                zombie.arrived = True

    def updateZombieDays(self):
        for zombie in self.zombies:
            zombie.zombieDays += 1

            if zombie.zombieDays > 15 and zombie.cell is not None:
                zombie.cell = None  # The zombie is <<death>>... again!

    def desactivateZombies(self, numberOfZombies, cell):
        i = 0
        for zombie in self.zombies:
            if zombie.cell == cell:
                zombie.cell = None  # The zombie is <<death>>... again!
                i += 1
                if i > numberOfZombies:
                    break

    def getZombiesToday(self, cell):
        totalZombies = 0
        for zombie in self.zombies:
            if zombie.cell == cell:
                totalZombies += 1

        return totalZombies

    def updateZombieArrived(self):
        for zombie in self.zombies:
            if zombie.cell is not None:
                zombie.arrived = False

    def printMatrix(self):
        self.number_image += 1
        matPrint = np.zeros([len(self.map), len(self.map[0])])
        matZombies = np.zeros([len(self.map), len(self.map[0])])

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                cell = self.map[x][y]
                if cell is not 0:
                    matPrint[x][y] = cell.population_today
                    matZombies[x][y] = self.getZombiesToday(cell)

        plt.imshow(matPrint, cmap='gray')
        plt.savefig("population" + str(self.number_image) + ".png")
        plt.imshow(matZombies, cmap='gray')
        plt.savefig("zombies" + str(self.number_image) + ".png")

    def noZombies(self):
        totalZombies = 0
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                cell = self.map[x][y]
                totalZombies += self.getZombiesToday(cell)

        if totalZombies == 0:
            print("All zombies are dead")
            return True
        return False

    def zombiesInBrest(self):
        cell = self.map[81][41]
        if self.getZombiesToday(cell):
            print("Zombies arrived to Brest in the day number: ", self.actualJour)

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                cell = self.map[x][y]
                cell.zombies = self.getZombiesToday(cell)
        np.save("brest.npy", self.map)

    def startApocalypse(self, endJour):
        while self.actualJour < endJour and not self.noZombies():
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]
                    neighbors = self.neighbors(x, y)

                    if self.getZombiesToday(cell) is not 0:
                        for neighbor in neighbors:
                            Hj = neighbor.population_today
                            Zj = self.getZombiesToday(cell)

                            if neighbor is not cell and Hj > 0:
                                # The formula for λd is as follows: λd is zero for a slope higher
                                # than 10 degrees, it is one for a slope of zero, and linear
                                # between these two values for slopes between 0 and 10 degrees.

                                elevationDiff = np.degrees(np.arctan(abs(cell.elevation - neighbor.elevation)/15000))
                                if elevationDiff > 10:
                                    lambdaFactor = 0
                                if elevationDiff == 0:
                                    lambdaFactor = 1
                                if 0 < elevationDiff <= 10:
                                    lambdaFactor = 1 - elevationDiff/10

                                zombiesToMove = int(abs((Hj / self.getTotalTodayPopulation(neighbors)) * Zj * lambdaFactor))
                                self.moveZombies(cell, neighbor, zombiesToMove)

                            if neighbor is cell and self.getTotalTodayPopulation(neighbors) == 0:
                                zombiesToMove = self.getZombiesToday(cell)
                                self.moveZombies(cell, neighbor, zombiesToMove)

            # The day is over, so, I need update the zombie days to <<kill>> some deaths
            self.updateZombieDays()

            # Update all zombie status
            self.updateZombieArrived()

            # Step 2
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]
                    humansAlive = int(cell.population_today)

                    if (self.getZombiesToday(cell) * 10) > humansAlive:
                        # Create new zombies with the deaths
                        self.zombies.extend([Zombie(cell) for _ in range(humansAlive)])
                        cell.population_today = 0
                    else:
                        # Create new zombies with the deaths
                        self.zombies.extend([Zombie(cell) for _ in range(self.getZombiesToday(cell) * 10)])
                        cell.population_today = humansAlive - self.getZombiesToday(cell) * 10

            # Step 3
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]
                    zombiesAlive = self.getZombiesToday(cell)
                    zombiesDie = 0
                    if cell.population_today > 0:
                        if zombiesAlive is not 0:
                            zombiesDie = int(abs(self.getZombiesToday(cell) - cell.population_today * 10))

                    if zombiesDie > self.getZombiesToday(cell):
                        self.desactivateZombies(zombiesAlive, cell)
                    elif zombiesAlive > zombiesDie > 0:
                        self.desactivateZombies(zombiesDie, cell)

            self.printMatrix()

            if self.actualJour % 10:
                for x in range(len(self.map)):
                    for y in range(len(self.map[x])):
                        cell = self.map[x][y]
                        cell.zombies = self.getZombiesToday(cell)
                np.save("matrix" + str(self.actualJour) + "days.npy", self.map)

            print("Day done: ", self.actualJour)
            self.actualJour += 1
            self.zombiesInBrest()

            # Final test
            # for x in range(len(self.map)):
            #     for y in range(len(self.map[x])):
            #         cell = self.map[x][y]
            #         zombiesAlive = self.getZombiesToday(cell)
            #         print("Cell: ", x, y, " - Zombies: ", zombiesAlive, " - Humans alive: ", cell.population_today)

    def neighbors(self, row, col, radius=1):
        row = row + 1
        col = col + 1
        rows, cols = len(self.map), len(self.map[0])
        neighbors = []

        for i in range(row - radius - 1, row + radius):
            for j in range(col - radius - 1, col + radius):

                if 0 <= i < rows and 0 <= j < cols:
                    neighbors.append(self.map[i][j])

        return neighbors
