import pandas as pd
import Location
from Distances import Matrix
from Truck import Truck

###############################################
         ###Fixed Data Points ###
###############################################

#Initialize Distances
Distances = Matrix("Matrix.csv")

#Initialize Facilities
locations = Location.Initialize('FacilityDemandInventory.csv')


###############################################
         ###Initial Deliveries(Capped Out) ###
###############################################

for i in range(len(locations)):
    if locations[i][2] > Truck.TotalCapacity:
        Truckcount = locations[i][2] // Truck.TotalCapacity
        locations[i][2] = locations[i][2] % Truck.TotalCapacity
#Initialize Trucks
