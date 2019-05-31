import matplotlib.pyplot as plt
import numpy as np


class Cell(object):
    def __init__(self, elevation, population):
        self.elevation = elevation
        self.population_today = population
        self.zombies = 0
        self.brest = False
        self.rize = False
        self.xCord = 0
        self.yCord = 0


class Zombie(object):
    def __init__(self, cell=None):
        self.zombieDays = 0
        self.cell = cell
        self.arrived = False


class Map(object):

    def __init__(self, map, zombies):
        self.map = map
        self.actualJour = 0
        self.zombies = zombies
        self.number_image = 0
        self.zombiesToMove = []
        self.brest = None

    def getTotalNeighborsPopulation(self, cell):
        total_population = 0
        for neighbor in self.map.neighbors(cell):
            total_population += neighbor.population_today

        return total_population

    def moveZombies(self, cellOrigin, cellDest):
        #print("CANTIDAD DE ZOMBIES ORIGINAL:", cellOrigin)
        for zombie, cell in self.zombies.items():
            if cell == cellOrigin:
                zombie.cell = cellDest
                zombie.arrived = True

                if cellOrigin.zombies > 0:
                    cellOrigin.zombies -= 1
                print("Zombie de ", cellOrigin.xCord, cellOrigin.yCord, "a la celda:", cellDest.xCord, cellDest.yCord)
                cellDest.zombies += 1
                self.zombiesToMove.append(zombie)
                # zombie.update(zombie) Creo que esto no hace falta

    def updateZombieDays(self):
        zombiesDie = []
        for zombie, cell in self.zombies.items():
            if zombie.zombieDays > 15 and cell.zombies > 0:
                cell.zombies -= 1
                zombiesDie.append(zombie)
            else:
                zombie.zombieDays += 1

        for zombie in zombiesDie:
            self.zombies.pop(zombie)  # The zombie is <<death>>... again!
        zombiesDie.clear()

    def killZombies(self, numberOfZombies, cell):
        i = 0
        zombiesDie = []
        for zombie in self.zombies:
            if zombie.cell == cell and cell.zombies > 0:
                zombiesDie.append(zombie)
                cell.zombies -= 1
                i += 1
                if i > numberOfZombies:
                    break

        for zombie in zombiesDie:
            self.zombies.pop(zombie)  # The zombie is <<death>>... again!
        zombiesDie.clear()

    def updateZombieArrived(self):
        for zombie in self.zombiesToMove:
            zombie.arrived = False
        self.zombiesToMove.clear()

    def noZombies(self):
        if not self.zombies:
            print("All zombies are dead")
            return True
        return False

    def zombiesInBrest(self):
        if self.brest is not None:
            if self.brest.zombies is not 0:
                print("Zombies arrived to Brest in the day number: ", self.actualJour)
                np.save("zombiesBrest" + str(self.actualJour) + "Days.npy", self.map)

    def startApocalypse(self, endJour):
        # Save Brest Cell
        if self.brest is None:
            for cell in self.map:
                if cell.brest:
                    self.brest = cell

        while self.actualJour < endJour and not self.noZombies():
            for cell in self.map:
                if cell.zombies is not 0:
                    Zj = int(cell.zombies)
                    for neighbor in self.map.neighbors(cell):
                        Hj = neighbor.population_today
                        # print("Poblacion vecinos:", neighbor.population_today)

                        totalNeighborsPopulation = self.getTotalNeighborsPopulation(cell)
                        print("ESTOY EN UN VECINO")
                        if Hj > 0:
                            print("ESTOY EN UN VECINaaaa")
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
                            # print("lambda:", lambdaFactor)
                            # print("Entro a mover")
                            # print("Total:", totalNeighborsPopulation)
                            # print("Zj", Zj)
                            # print("Hj", Hj)
                            #
                            # print("division rqrq:", (Hj / totalNeighborsPopulation) * Zj)
                            zombiesToWalk = int((Hj / totalNeighborsPopulation) * Zj * lambdaFactor)
                            print("Zombies en celda padre:", Zj)
                            print("Pasan estos zombies:", zombiesToWalk)

                            for i in range(zombiesToWalk):
                                self.moveZombies(cell, neighbor)
                        if totalNeighborsPopulation == 0:
                            print("ESTOY EN UN VECINaaaa ééééé")
                            for i in range(cell.zombies):
                                self.moveZombies(cell, neighbor)

            # Update all zombie status
            self.updateZombieArrived()

            # Step 2 and Step 3
            for cell in self.map:
                if cell.zombies > 0:
                    humansAlive = int(cell.population_today)
                    if (cell.zombies * 10) > humansAlive:
                        # Create new zombies with the deaths
                        for _ in range(humansAlive):
                            cell.zombies += 1
                            self.zombies.update({Zombie(): cell})
                        cell.population_today = 0

                    else:
                        # Create new zombies with the deaths
                        for _ in range(cell.zombies * 10):
                            cell.zombies += 1
                            self.zombies.update({Zombie(): cell})
                        cell.population_today = humansAlive - cell.zombies * 10

                        # Humans kill zombies
                        zombiesDie = int(abs(cell.zombies - cell.population_today * 10))
                        if zombiesDie > cell.zombies:
                            self.killZombies(cell.zombies, cell)
                        elif cell.zombies > zombiesDie > 0:
                            self.killZombies(zombiesDie, cell)

            if self.actualJour % 10:
                np.save("graph" + str(self.actualJour) + "days.npy", self.map)

            # The day is over, so, I need update the zombie days to <<kill>> some deaths
            self.updateZombieDays()
            self.actualJour += 1
            self.zombiesInBrest()
            print("Day done: ", self.actualJour)

            totalZombies = 0
            for cell in self.map:
                totalZombies += cell.zombies
            print(totalZombies)

            # Final test
            # for x in range(len(self.map)):
            #     for y in range(len(self.map[x])):
            #         cell = self.map[x][y]
            #         zombiesAlive = cell.zombies
            #         print("Cell: ", x, y, " - Zombies: ", zombiesAlive, " - Humans alive: ", cell.population_today)
