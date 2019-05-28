from Map import *


def main():
    cellZombie = Cell(0, 0)
    # cellZombie.addZombiesToCell(5)

    matrix = [
        [Cell(0, 0), Cell(0, 0), Cell(0, 0)],
        [Cell(0, 0), cellZombie, Cell(0, 0)],
        [Cell(0, 0), Cell(0, 0), Cell(0, 0)]]

    # Creo dos zombies en la celda
    zombie1 = Zombie(cellZombie)
    zombie2 = Zombie(cellZombie)

    map = Map(matrix, [zombie1, zombie2])

    # Test para ver que los vecinos de una posicion se obtienen correctamente <3
    print("Tengo esta cantidad de vecinos: ", len(map.neighbors(2, 2)))
    print(map.neighbors(2, 2))

    # Test apocalypse de un dia
    map.startApocalypse(1)

    print("A ver como quedo todo:")
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            cell = matrix[x][y]
            print("Coordenada (x,y): ", x, ",", y)
            print("Poblacion: ", cell.population_today)
            print("Zombies:", map.getZombiesToday(cell))


if __name__ == '__main__':
    main()
