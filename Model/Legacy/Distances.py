import numpy as np
class Matrix():
    def __init__(self,file):
        #Distances from all locations to all locations
        #Matrix Will be organized and square so that row i is the same location as col i
        #this means means each location can have its own unique ID from 0 to n
        # We can ref each unique distance as a index of the locations order independent
        return(np.loadtxt(file, delimiter=','))

    def Findmileage(matrix, start,end):
        return(matrix[start][end])
