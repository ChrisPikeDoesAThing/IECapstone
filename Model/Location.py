class Location():
    def __init__(self,inventory,demand):
        self.Inventory = inventory
        self.Demand = demand
        
    def transport(self,units):
        self.Inventory += units
        self.Demand = self.Demand - self.Inventory
        