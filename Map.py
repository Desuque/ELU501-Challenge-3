import matplotlib.pyplot as plt
import numpy as np
from heapq import heappop as pop
from heapq import heappush as push
import networkx as nx


class Cell(object):
    """
    # Object to create cells
    #  input : elevation: int, population, int
    #  output: cell with elevation and population, with no zombies
    """
    def __init__(self, elevation, population):
        self.elevation = elevation
        self.population_today = population
        self.zombies = 0
        self.brest = False
        self.rize = False
        self.xCord = 0
        self.yCord = 0


class Zombie(object):
    """
    # Object to create zombies
    #  input : the cell to add new zombies
    #  output: zombie with 0 days of life
    """
    def __init__(self, cell=None):
        self.zombieDays = 0
        self.cell = cell
        self.arrived = False


class Map(object):
    """
    # Object to create the complete map with all information
    #  input : map: graph, zombies: list[Zombie]
    #  output: -
    """
    def __init__(self, map, zombies):
        self.map = map
        self.actualJour = 0
        self.zombies = zombies
        self.number_image = 0
        self.zombiesToMove = []
        self.brest = None

    """
    # Function to get all neighbors from cell
    #  input : cell: Cell
    #  output: totalNeighbors: int
    """
    def getTotalNeighborsPopulation(self, cell):
        total_population = 0
        for neighbor in self.map.neighbors(cell):
            total_population += neighbor.population_today

        return total_population

    """
    # Function to move zombies from origin to destination
    #  input : cellOrigin: Cell, cellDestination: Cell
    #  output: -
    """
    def moveZombies(self, cellOrigin, cellDest):
        for zombie, cell in self.zombies.items():
            if cell == cellOrigin and not zombie.arrived:
                zombie.cell = cellDest
                zombie.arrived = True

                if cellOrigin.zombies > 0:
                    cellOrigin.zombies -= 1
                cellDest.zombies += 1
                self.zombiesToMove.append(zombie)

    """
    # Function to update the zombie days (life days)
    #  input : -
    #  output: -
    """
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

    """
    # Function to kill zombies from a cell
    #  input : numberOfZombiesToKill: int, cellOrigin: Cell
    #  output: -
    """
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

    """
    # Function to update the status of a zombie (If the zombie has arrived or if
    the zombie is in way to arrive)
    #  input : -
    #  output: -
    """
    def updateZombieArrived(self):
        for zombie in self.zombiesToMove:
            zombie.arrived = False
        self.zombiesToMove.clear()

    """
    # Function know if all the zombies are dead
    #  input : -
    #  output: True/False
    """
    def noZombies(self):
        if not self.zombies:
            print("All zombies are dead")
            return True
        return False

    """
    # Function know if the zombies are in Brest
    #  input : -
    #  output: -
    """
    def zombiesInBrest(self):
        if self.brest is not None:
            if self.brest.zombies is not 0:
                print("Zombies arrived to Brest in the day number: ", self.actualJour)
                np.save("zombiesBrest" + str(self.actualJour) + "Days.npy", self.map)

    """
    # Function to start the apocalypse, its the start of all. We need to know how long is it going to last
    #  input : endJour: int
    #  output: -
    """
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
                    totalNeighborsPopulation = self.getTotalNeighborsPopulation(cell)

                    for neighbor in self.map.neighbors(cell):
                        Hj = neighbor.population_today

                        if Hj > 0:
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

                            zombiesToWalk = int((Hj / totalNeighborsPopulation) * Zj * lambdaFactor)

                            for i in range(zombiesToWalk):
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

            if self.actualJour % 10 == 0:
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

    """
    # Function to find the shortest way to arrive to Brest from Rize (Using Dijkstra Networkx)
    #  input : -
    #  output:  path – All returned paths include both the source and target in the path.
    #           Return type: list or dictionary
    """
    def Dikstra_implemented(self):
        for cell in self.map:
            if cell.rize:
                rize = cell
            if cell.brest:
                brest = cell

        return nx.shortest_path(self.map, rize, brest, default='dijkstra')

    """
    # Function to find the shortest way to arrive to Brest from Rize (Dijkstra)
    #  input : -
    #  output: -
    """
    def Dijkstra(self):
        i = 0
        heap = []
        rize_point = (137, 276)  # Rize
        brest_point = (81, 41)  # Brest
        push(heap, (self.map[rize_point], rize_point))
        rize = None
        distances = {}
        map_shape = self.map.shape
        for x in range(map_shape[0]):
            for y in range(map_shape[1]):
                distances[(x, y)] = float('inf')
        distances[rize_point] = 0

        for cell in self.map:
            if cell.rize:
                rize = cell

        while heap:
            thisWeight, thisNode = pop(heap)

            for nbr in self.map.neighbors(rize):
                distance_nbr = thisWeight + self.map[nbr]

                if distances[nbr] > distance_nbr:
                    distances[nbr] = distance_nbr
                    push(heap, (distance_nbr, nbr))
                    previous[nbr] = thisNode

            i += 1

        print("Take: ", distances[brest_point]/24, " days to arrive a Brest ")
