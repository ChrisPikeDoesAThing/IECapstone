import pandas as pd
from Location import Location

#Initialize Facilities
File = 'FacilityDemandInventory.csv'
data = pd.readcsv(File)
LocationObjs = []
for i in range(len(data)):
    LocationObjs.append(Location(data["inventory"],data["demand"]))
    

#Initialize Trucks