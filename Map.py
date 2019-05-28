
class Cell(object):
    def __init__(self, elevation, population):
        self.elevation = elevation
        self.population_today = population
        self.population_tomorrow = 0
        self.zombies_tomorrow = 0


class Zombie(object):
    def __init__(self, cell=None):
        self.zombieDays = 0
        self.cell = cell


class Map(object):

    def __init__(self, map, zombies):
        self.map = map
        self.initX = None
        self.initY = None
        self.actualJour = 0
        self.zombies = zombies

    def setInitialPoint(self, coordinates):
        self.initX = coordinates[0]
        self.initY = coordinates[1]

    def getTotalTodayPopulation(self, neighbors):
        total_population = 0
        for neighbor in neighbors:
            total_population += neighbor.population_today

        return total_population

    def moveZombies(self, cellOrigin, cellDest, numberToMove):
        zombiesPassed = 0
        for zombie in self.zombies:
            if zombie.cell == cellOrigin and zombiesPassed < numberToMove:
                print("Se mueven los zombies")
                zombie.cell = cellDest
                zombiesPassed += 1

    def updateZombieDays(self):
        for zombie in self.zombies:
            zombie.zombieDays += 1

            if zombie.zombieDays > 15 and zombie.cell is not None:
                zombie.cell = None  # The zombie is <<death>>... again!

    def desactivateZombies(self, numberOfZombies):
        i = 0
        for zombie in self.zombies:
            zombie.cell = None  # The zombie is <<death>>... again!
            i += 1
            if i > numberOfZombies:
                break

    def getZombiesToday(self, cell):
        totalZombies = 0
        for zombie in self.zombies:
            if zombie.cell == cell:
                totalZombies +=1

        return totalZombies

    def startApocalypse(self, endJour):
        while self.actualJour < endJour:
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]

                    print("Coordenada (x,y): ", x, ",", y)
                    print("Poblacion: ", cell.population_today)
                    print("Zombies:", self.getZombiesToday(cell))
                    print("")

                    # Obtengo todos los vecinos de una celda dada
                    neighbors = self.neighbors(x, y)

                    for neighbor in neighbors:
                        Hj = neighbor.population_today
                        Zj = self.getZombiesToday(neighbor)

                        if neighbor is not cell and Hj > 0:
                            print("CASO 1")
                            # The formula for λd is as follows: λd is zero for a slope higher
                            # than 10 degrees, it is one for a slope of zero, and linear
                            # between these two values for slopes between 0 and 10 degrees.

                            elevationDiff = abs(cell.elevation - neighbor.elevation)
                            if elevationDiff > 10:
                                lambdaFactor = 0
                            if elevationDiff == 0:
                                lambdaFactor = 1
                            if 0 < lambdaFactor <= 10:
                                lambdaFactor == elevationDiff / 10

                            neighbor.zombies_tomorrow += (Hj / self.getTotalTodayPopulation(neighbors)) * Zj * lambdaFactor
                            self.moveZombies(cell, neighbor)

                        if neighbor is not cell and Hj == 0:
                            print("CASO 2")
                            neighbor.zombies_tomorrow += 0

                        if neighbor is cell and self.getTotalTodayPopulation(neighbors) > 0:
                            print("CASO 3")
                            neighbor.zombies_tomorrow += 0

                        if neighbor is cell and self.getTotalTodayPopulation(neighbors) == 0:
                            print("CASO 4")
                            neighbor.zombies_tomorrow += Zj
                            print("Cantidad a mover:", Zj)
                            self.moveZombies(cell, neighbor, Zj)

                    # The day is end, update zombies with zombies of tomorrow and set
                    # them to zero
                    for neighbor in neighbors:
                        neighbor.zombies_today = neighbor.zombies_tomorrow
                        neighbor.zombies_tomorrow = 0

                    # The day is over, so, I need update the zombie days to <<kill>> some deaths
                    self.updateZombieDays()

            # Step 2
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]
                    print("A ver que tiene la celda; ", cell)
                    humansAlive = cell.population_today
                    humansDies = cell.population_today - self.getZombiesToday(cell) * 10

                    if humansDies >= cell.population_today:
                        cell.population_today = 0
                        # Create new zombies with the deaths
                        self.zombies.extend([Zombie(cell) for _ in range(humansAlive)])
                    else:
                        cell.population_today = humansDies
                        # Create new zombies with the deaths
                        self.zombies.extend([Zombie(cell) for _ in range(humansDies)])

            # Step 3
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    cell = self.map[x][y]
                    zombiesAlive = self.getZombiesToday(cell)
                    zombiesDie = self.getZombiesToday(cell) - cell.population_today * 10

                    if zombiesDie >= self.getZombiesToday(cell):
                        self.desactivateZombies(zombiesAlive)
                    else:
                        self.desactivateZombies(zombiesDie)

            self.actualJour += 1

    def neighbors(self, row, col, radius=1):
        rows, cols = len(self.map), len(self.map[0])
        neighbors = []

        for i in range(row - radius - 1, row + radius):
            for j in range(col - radius - 1, col + radius):

                if 0 <= i < rows and 0 <= j < cols:
                    neighbors.append(self.map[i][j])

        return neighbors
