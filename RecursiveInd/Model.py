
def FindOptimalDist():
    for facility in facilitylist:
        # Find list of distances from Facility to all locations:
        #Sort by proximity (Lowest to highest)
        #Fill Demand Starting with Cheapest.