from PIL import Image
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from Map import *

from matplotlib import pyplot as plt
import struct



def main():

    #Processing of the population density image

    population_density = "/homes/g18quint/PycharmProjects/ELU501-Challenge-3/population-density-map.bmp"

    maxDensity = 3000  # hab/km2

    densityMatrix = popDensityScaling(population_density,maxDensity)

    #densityMatrix = densityMatrix[0:1000, 0:1000]

    print("density matrix shape : ", np.shape(densityMatrix))

    #plt.imshow(densityMatrix,cmap='gray')
    #plt.show()

    # Processing of the elevation image

    elevation = "/homes/g18quint/PycharmProjects/ELU501-Challenge-3/elevation1x1_new-mer-bleue.bmp"



    maxElevation = 4810 #elevation of the Mont Blanc

    pixelMaxElevation = searchMaxAltitude(elevation)

    elevationRotated = "/homes/g18quint/PycharmProjects/ELU501-Challenge-3/elevation1x1_new-mer-bleue.bmp"

    elevationMatrix = elevationScaling(elevationRotated,maxElevation,pixelMaxElevation)

    im = elevationMatrix
    plt.imshow(im,cmap='gray')
    plt.show()

    print("elev matrix shape : ", np.shape(elevationMatrix))

    deltX = 1000
    deltaY = 0
    elevationMatrixCut = elevationMatrix[deltX:(deltX+3510),deltaY:(deltaY+4251)]

    plt.imshow(elevationMatrixCut,cmap='gray')
    plt.show()
    print("elev matrix shape : ", np.shape(elevationMatrixCut))

    #Graph creation

    picture,graph = createGraph(densityMatrix,elevationMatrixCut,15,2)

    print("shape graphe ",np.shape(picture[:,:,0]))

    im = picture[:,:,0]
    plt.imshow(im,cmap='gray')
    plt.show()

    im = picture[:,:,1]
    plt.imshow(im,cmap='gray')
    plt.show()

    #we save the graph in a numpy file
    np.save("graph.npy",graph)

    #we load the graph
    loadedGraph = np.load("graph.npy",allow_pickle=True)
    print("node ",loadedGraph[100,100])
    print("node population ", loadedGraph[100, 100].population_today)
    print("node elevation : ", loadedGraph[100, 100].elevation)

def createGraph(imgPop,imgElev,numberOfPixels,charac):

    heightOriginal1,widthOriginal1 = np.shape(imgPop)
    heightOriginal2, widthOriginal2 = np.shape(imgElev)
    heightOriginal = min(heightOriginal1,heightOriginal2)
    widthOriginal = min(widthOriginal1,widthOriginal2)
    height = int(np.floor(heightOriginal/numberOfPixels))
    width = int(np.floor(widthOriginal / numberOfPixels))

    graph = np.zeros([height,width,charac])
    #graphMatrix = np.zeros([height,width,charac])
    graphMatrix = np.full((height, width), Cell(0,0))
    for i in range(height):
        for j in range(width):
            line = i*(numberOfPixels+1)
            column = j * (numberOfPixels+1)
            graph[i, j, 0] = np.sum(imgPop[line:(line+numberOfPixels), column:(column+numberOfPixels)]) / (numberOfPixels ** 2)
            graph[i, j, 1] = np.sum(imgElev[line:(line + numberOfPixels), column:(column + numberOfPixels)]) / (numberOfPixels ** 2)
            graphMatrix[i,j] = Cell(graph[i, j, 1],graph[i, j, 0])
            """
            if i<5 and j<5:
                print("matriz original" ,imgPop[i:(i+numberOfPixels), j:(j+numberOfPixels)])
                print("grafo " ,graph[i, j, 0])
            """
    return graph,graphMatrix






def popDensityScaling(path,maxDensity):

    im = Image.open(path)

    width = im.size[0]
    heigth = im.size[1]

    grayim = im.convert("L")
    #grayim.show()
    colors = grayim.getcolors(width * heigth)
    #print('Nb of different colors: %d' % len(colors))
    # With the image im, let's generate a numpy array to manipulate pixels
    p = np.array(grayim)
    # plot the histogram. We still have a lot of dark colors. Just to check ;-)
    #h = np.histogram(p.ravel())
    #plt.show(h)
    # from gray colors to density
    density = p / 255.0*maxDensity
    #print(density)
    # plot the histogram. We still have a lot of dark colors. Just to check ;-)
    #d2 = density.ravel()

    #print(np.shape(d2))

    #plt.hist(density.ravel())

    return density

def elevationScalingLouis(path):

    im = Image.open(path)

    width = im.size[0]
    heigth = im.size[1]

    colours = im.getcolors(width * heigth)
    L = len(colours)
    print('Nb of different colors: %d' % len(colours))

    RGBsorted=list(colours)
    RGBsorted.sort()
    #print(RGBsorted)

    #Luigi

    colours_length = len(colours)
    colours = [c[1] for c in colours]
    A = np.zeros([colours_length, colours_length])
    print('arranca el for')
    for x in range(0, colours_length):
        for y in range(0, colours_length):
            A[x, y] = distance.euclidean(colours[x], colours[y])

    def NN(A, start):
        """Nearest neighbor algorithm.
        A is an NxN array indicating distance between N locations
        start is the index of the starting location
        Returns the path and cost of the found solution
        """
        path = [start]
        cost = 0
        N = A.shape[0]
        mask = np.ones(N, dtype=bool)  # boolean values indicating which
        # locations have not been visited
        mask[start] = False
        for i in range(N - 1):
            last = path[-1]
            next_ind = np.argmin(A[last][mask])  # find minimum of remaining locations
            next_loc = np.arange(N)[mask][next_ind]  # convert to original location
            path.append(next_loc)
            mask[next_loc] = False
            cost += A[last, next_loc]
        return path, cost

    path, _ = NN(A, 0)
    # Final array
    colours_nn = []
    for i in path:
        colours_nn.append(colours[i])
    sortedColors = list(colours_nn)
    misplaced = sortedColors.pop(-2)
    sClrs = []
    sClrs.append(sortedColors[0])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[1:])
    sortedColors = sClrs
    sClrs = []
    misplaced = sortedColors.pop(-1)
    sClrs.extend(sortedColors[:sortedColors.index((238, 232, 172))])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[sortedColors.index((238, 232, 172)):])
    sortedColors = sClrs
    displNN = Image.new("RGB", (L, 1))
    displNN.putdata(sortedColors)
    displNN = displNN.resize((8 * L, 500))
    displNN.show() #BEST RESULT
    altitudes = [(i * 4.810) / (L - 1) for i in range(0, L)]
    map_color_altitude = dict(zip(sortedColors, altitudes))
    map_color_altitude[(0, 0, 0)] = 0

    def closest_color(color, colors):
        colors = np.asarray(colors)
        deltas = colors - color
        dist = np.einsum('ij,ij->i', deltas, deltas)
        c = colors[np.argmin(dist)]
        return (c[0], c[1], c[2])


    return map_color_altitude

def searchMaxAltitude(path):

    im = Image.open(path)

    print(im.size)

    width = im.size[0]
    heigth = im.size[1]

    colours = im.getcolors(width * heigth)
    L = len(colours)

    RGBsorted = list(colours)
    RGBsorted.sort()
    print(RGBsorted)

    # Luigi

    colours_length = len(colours)
    colours = [c[1] for c in colours]
    A = np.zeros([colours_length, colours_length])
    for x in range(0, colours_length):
        for y in range(0, colours_length):
            A[x, y] = distance.euclidean(colours[x], colours[y])

    def NN(A, start):
        """Nearest neighbor algorithm.
        A is an NxN array indicating distance between N locations
        start is the index of the starting location
        Returns the path and cost of the found solution
        """
        path = [start]
        cost = 0
        N = A.shape[0]
        mask = np.ones(N, dtype=bool)  # boolean values indicating which
        # locations have not been visited
        mask[start] = False
        for i in range(N - 1):
            last = path[-1]
            next_ind = np.argmin(A[last][mask])  # find minimum of remaining locations
            next_loc = np.arange(N)[mask][next_ind]  # convert to original location
            path.append(next_loc)
            mask[next_loc] = False
            cost += A[last, next_loc]
        return path, cost

    path, _ = NN(A, 0)
    print(path)
    # Final array
    colours_nn = []
    for i in path:
        colours_nn.append(colours[i])
    sortedColors = list(colours_nn)
    misplaced = sortedColors.pop(-2)
    sClrs = []
    sClrs.append(sortedColors[0])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[1:])
    sortedColors = sClrs
    sClrs = []
    misplaced = sortedColors.pop(-1)
    sClrs.extend(sortedColors[:sortedColors.index((238, 232, 172))])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[sortedColors.index((238, 232, 172)):])
    sortedColors = sClrs

    return sortedColors[-1]


def elevationScaling(path,maxAltitude,maxColour):

    im = Image.open(path)

    width = im.size[0]
    heigth = im.size[1]

    colours = im.getcolors(width * heigth)
    L = len(colours)

    RGBsorted=list(colours)
    RGBsorted.sort()
    #print(RGBsorted)

    #Luigi

    colours_length = len(colours)
    colours = [c[1] for c in colours]
    A = np.zeros([colours_length, colours_length])
    for x in range(0, colours_length):
        for y in range(0, colours_length):
            A[x, y] = distance.euclidean(colours[x], colours[y])

    def NN(A, start):
        """Nearest neighbor algorithm.
        A is an NxN array indicating distance between N locations
        start is the index of the starting location
        Returns the path and cost of the found solution
        """
        path = [start]
        cost = 0
        N = A.shape[0]
        mask = np.ones(N, dtype=bool)  # boolean values indicating which
        # locations have not been visited
        mask[start] = False
        for i in range(N - 1):
            last = path[-1]
            next_ind = np.argmin(A[last][mask])  # find minimum of remaining locations
            next_loc = np.arange(N)[mask][next_ind]  # convert to original location
            path.append(next_loc)
            mask[next_loc] = False
            cost += A[last, next_loc]
        return path, cost

    path, _ = NN(A, 0)
    #print(path)
    # Final array
    colours_nn = []
    for i in path:
        colours_nn.append(colours[i])
    sortedColors = list(colours_nn)
    misplaced = sortedColors.pop(-2)
    sClrs = []
    sClrs.append(sortedColors[0])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[1:])
    sortedColors = sClrs
    sClrs = []
    misplaced = sortedColors.pop(-1)
    sClrs.extend(sortedColors[:sortedColors.index((238, 232, 172))])
    sClrs.append(misplaced)
    sClrs.extend(sortedColors[sortedColors.index((238, 232, 172)):])
    sortedColors = sClrs

    if maxColour != sortedColors[-1]:
        sortedColors.append(maxColour)
        L = len(sortedColors)

    displNN = Image.new("RGB", (len(sortedColors), 1))
    displNN.putdata(sortedColors)
    displNN = displNN.resize((8 * L, 500))
    #displNN.show() #BEST RESULT
    altitudes = [(i * maxAltitude) / (L - 1) for i in range(0, L)]
    map_color_altitude = dict(zip(sortedColors, altitudes))
    print('map color altitude: ',map_color_altitude)
    print('map color altitude shape: ',np.shape(map_color_altitude))
    map_color_altitude[(0, 0, 0)] = 0
    print("altitudes", altitudes)

    print("width ", im.size[0])
    print("height ", im.size[1])


    rgb_im = im.convert('RGB')
    #rgb_im = rgb_im.rotate(90)
    rgb_im = rgb_im.transpose(Image.FLIP_LEFT_RIGHT)
    rgb_im = rgb_im.rotate(90)

    elevMap = np.zeros([width,heigth])
    for i in range(width-1):
        for j in range(heigth-1):
            r, g, b = rgb_im.getpixel((i, j))
            elevMap[i,j] = map_color_altitude.get((r,g,b))

    return elevMap

    def closest_color(color, colors):
        colors = np.asarray(colors)
        deltas = colors - color
        dist = np.einsum('ij,ij->i', deltas, deltas)
        c = colors[np.argmin(dist)]
        return (c[0], c[1], c[2])



if __name__ == '__main__':
    main()
