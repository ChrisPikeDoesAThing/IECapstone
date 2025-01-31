#Minimize
from Constants import Constant

def RouteCost(Route):
    X =  Route  #Bottles transported over distance
    Mileage = Route#Mileage over which bottles are transported
    cost = 0
    for i in range(len(Route)):
        cost += (Constant.tonmile * ((Constant.bottlevolume / 16) * Route[i][1] ) * Constant.ton) * Mileage