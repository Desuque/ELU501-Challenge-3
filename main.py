from PIL import Image
import numpy as np
from scipy.spatial import distance

from matplotlib import pyplot as plt
import struct



def main():

    #Processing of the population density image

    population_density = "/homes/g18quint/PycharmProjects/ELU501-Challenge-3/population-density-map.bmp"

    maxDensity = 3000  # hab/km2

    densityMatrix = popDensityScaling(population_density,maxDensity)

    # Processing of the elevation image

    elevation = "/homes/g18quint/PycharmProjects/ELU501-Challenge-3/elevation1x1_new-mer-bleue.bmp"

    maxElevation = 4810 #elevation of the Mont Blanc

    pixelMaxElevation = searchMaxAltitude(elevation)

    elevationMatrix = elevationScaling(elevation,maxElevation,pixelMaxElevation)


def __init__(self, pixels, pixels_elevation, row, col):
    self.pixels=pixels
    self.tmp=[]
    for i in range(15):
        for j in range(15):
            self.tmp.append((self.pixels[i][j][0],self.pixels[i][j][1],self.pixels[i][j][2]))
    self.pop_dens=math.floor(sum([map_color_density2[p] for p in self.tmp]))
    self.tmp2=[]
    self.zombies=[]
    #for i in range(15):
    #    for j in range(15):
    #        self.tmp2.append((pixels_elevation[i][j][0],pixels_elevation[i][j][1],pixels_elevation[i][j][2]))
    #self.elevation=np.mean([map_color_altitude[closest_color(p,sortedColors)] for p in self.tmp2])
    self.id=Cell.id
    self.row = self.id//234
    self.col = self.id-234*(self.id//234)
    Cell.id+=1
    #Cell.cells[self.row][self.col]=self
    Cell.tempcells.append(self)

def createGraph(imgPop,imgElev,numberOfPixels,charac):

    heightOriginal,widhtOriginal = np.shape(imgPop) #the images need to have the same shape
    height = np.floor(heightOriginal/numberOfPixels)
    widht = np.floor(widhtOriginal / numberOfPixels)

    graph = np.zeros((height,widht,charac))

    counter = 0
    i=0
    j=0
    for line in range(widhtOriginal):
        for column in range(heightOriginal):
            acumulatedPop + = imgPop[line,column]
            acumulatedElev + = imgElev[line, column]
            counter + = 1
            if counter == numberOfPixels:
                graph[i,j,0] = acumulatedPop / (numberOfPixels**2)
                graph[i, j,1] = acumulatedElev / (numberOfPixels ** 2)






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
    print(RGBsorted)

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
    print(RGBsorted)

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

    if maxColour != sortedColors[-1]:
        sortedColors.append(maxColour)
        L = len(sortedColors)

    displNN = Image.new("RGB", (len(sortedColors), 1))
    displNN.putdata(sortedColors)
    displNN = displNN.resize((8 * L, 500))
    displNN.show() #BEST RESULT
    altitudes = [(i * maxAltitude) / (L - 1) for i in range(0, L)]
    map_color_altitude = dict(zip(sortedColors, altitudes))
    print('map color altitude: ',map_color_altitude)
    print('map color altitude shape: ',np.shape(map_color_altitude))
    map_color_altitude[(0, 0, 0)] = 0

    return map_color_altitude

    def closest_color(color, colors):
        colors = np.asarray(colors)
        deltas = colors - color
        dist = np.einsum('ij,ij->i', deltas, deltas)
        c = colors[np.argmin(dist)]
        return (c[0], c[1], c[2])



if __name__ == '__main__':
    main()
