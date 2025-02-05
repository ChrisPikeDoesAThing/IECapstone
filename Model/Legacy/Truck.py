class Truck():
    TotalCapacity = 41880
    def __init__(self, capacity, route):
        #### Route should follow form [[i,x],[i+1,x],[]]
        self.capacity = capacity
        self.Route = route
        
        
        