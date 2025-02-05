#Minimize
from Constants import Constant
from Distances import Findmileage

def RouteCost(Route):
    #Route[i][0] = Start
    #Route[i+1][0] = End
    #Route[i][1] = Number of Bottles
    cost = 0
    for i in range(len(Route)):
        mileage = Findmileage(Route[i][0],Route[i+1][0])
        
        cost += (Constant.tonmile * ((Constant.bottlevolume / 16) * Route[i][1] ) * Constant.ton) * mileage