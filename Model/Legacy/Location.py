import pandas as pd
class Location():
    def __init__(self,id,inventory,demand):
        self.Id = id
        self.Inventory = inventory
        self.Demand = demand
        
    def transport(self,units):
        self.Inventory += units
        self.Demand = self.Demand - self.Inventory
        
def Initialize(file):
    data = pd.readcsv(file)
    LocationObjs = []
    for i in range(len(data)):
        LocationObjs.append(Location(data[i][0],data[i][2], data[i][3]))
    return(LocationObjs)