import numpy as np

Distfile = 'distancematrix.csv'
#Distances from all locations to all locations


#Matrix Will be organized and square so that row i is the same location as col i
#this means means each location can have its own unique ID from 0 to n
# We can ref each unique distance as a index of the locations order independent


distancematrix = np.loadtxt(Distfile, delimiter=',')



def Findmileage(start,end):
    return(distancematrix[start][end])