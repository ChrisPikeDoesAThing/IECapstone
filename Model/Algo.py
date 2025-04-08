import os
import pandas as pd
import numpy as np
import csv
import random
import math

#########################################
###### FILE Modification Functions ######
#########################################


def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

def read_csv_to_list(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def get_element_by_keys(list_of_lists, first_key, second_key,element = 2):
   
    for inner_list in list_of_lists:
        if (int(inner_list[0]) == first_key) and (int(inner_list[1]) == second_key):
            return inner_list[element]
    return None

def convert_third_item_to_int(list_of_lists):
    for inner_list in list_of_lists:
        inner_list[2] = round(float(inner_list[2]))
    return list_of_lists

def sort_dicts_by_value(dict_list,value):
    return sorted(dict_list, key=lambda x: x.Inventory)

def csv_to_dict_list(csv_file_path, has_headers=0):
    dict_list = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in range(has_headers):
            next(csv_reader)
        for row in csv_reader:
            row_dict = {i: row[i] for i in range(len(row))}
            dict_list.append(row_dict)
    return dict_list

def filter_facilitylist_by_id(facilitylist, id_number):

    return [facility for facility in facilitylist if facility[0] == str(id_number)]

def sort_list_of_lists_by_column(data, column_index,reverse=False):
    return sorted(data, key=lambda x: x[column_index], reverse=reverse)

def subtract_from_third_key(dict_list, key_value, subtract_value, subtractindex=2):
    for row in dict_list:
        if row[0] == key_value:
            row[2] = str(float(row[subtractindex]) - subtract_value)
            break
    return dict_list

def get_key_value_by_second_key(dict_list, second_key_value,val0 = 0, val1 = 2):
    for row in dict_list:
        if row[val0] == str(second_key_value):
            return row[val1]
    return None
#################################################
###### End of File Modification Functions #######
#################################################


class Location():

    def __init__(self,id,name,inventory,latitude=None,longitude=None):
        self.Id = int(id)
        self.Name = str(name)
        self.Latitude = latitude
        self.Longitude = longitude
        self.Inventory = inventory

def InitializeLocations(Supply, Demand, LatLong, iteration = None): ### Initialize Locations

    ### Load CSVS
    Supply = csv_to_dict_list(join_path(Supply), has_headers=1)
    Demand = csv_to_dict_list(join_path(Demand), has_headers=1)
    LatLong = csv_to_dict_list(join_path(LatLong), has_headers=0)
    Locations = []
    Suppliers = []
    Counties = []
    ### Create Location Objects
    for supply in Supply:
        location = Location(supply[0],supply[1], int(float(supply[2])),LatLong[int(supply[0])][2],LatLong[int(supply[0])][3])
        Locations.append(location)
        Suppliers.append(location)
    for demand in Demand:
        location = Location(demand[0],demand[1], -1*int(float(demand[2])),LatLong[int(demand[0])][2],LatLong[int(demand[0])][3])
        Locations.append(location)
        Counties.append(location)

    ### Sort/Randomize Location Order
    if iteration is not None:
        Suppliers = sort_dicts_by_value(Suppliers,2)
    else:
        random.shuffle(Suppliers)
    return Locations,Suppliers,Counties

def Trial(supplypath,demandpath,latlongpath, facilitylist,iteration = None,Mtype = "Transparent",method="distance"):
    Locations,Supply,Demand = InitializeLocations(supplypath,demandpath,latlongpath,iteration) ### Initialize Locations
    Distribution = []
    qtysum = 0
    if method == "distance":
            method = 2
    elif method == "time":
        method = 3

    for supplier in Supply: ### Iterate through suppliers
        filtered_facilities = sorted(filter_facilitylist_by_id(facilitylist, supplier.Id), key=lambda x: x[method]) ### Filter by supplier Id and Sort by distance/time
        for facility in filtered_facilities:
            demander = int(facility[1]) ### Get Demander Id
            distributionqty = 0
            if (Locations[demander].Inventory < 0) and (Locations[supplier.Id].Inventory > 0): ### If Demand is not met

                #Cases
                if Locations[supplier.Id].Inventory > abs(Locations[demander].Inventory): # Completely fills demand / more supply

                    distributionqty += abs(Locations[demander].Inventory) # Add to distribution
                    Locations[supplier.Id].Inventory += Locations[demander].Inventory # Subtract from supply
                    Locations[demander].Inventory = 0 # Set demand to 0

                if Locations[supplier.Id].Inventory == Locations[demander].Inventory: # Completely fills demand / no more supply

                    distributionqty += abs(Locations[demander].Inventory)
                    Locations[supplier.Id].Inventory = 0
                    Locations[demander].Inventory = 0
                
                if Locations[supplier.Id].Inventory < abs(Locations[demander].Inventory): # Partially fills demand / no more supply

                    distributionqty += abs(Locations[supplier.Id].Inventory)
                    Locations[demander].Inventory += Locations[supplier.Id].Inventory
                    Locations[supplier.Id].Inventory = 0
                #print(Locations[supplier.Id].Inventory)
            if distributionqty > 0:
                Distribution.append([supplier.Id,demander,distributionqty])
                if Mtype != "Transparent":
                    Locations[demander].Inventory -= distributionqty
    return Locations,Distribution
 

def EvaluateDistribution(Distribution,facilitylist): ### Evaluate Distribution
    ### Initialize Variables
    costsum = 0
    cost_per_mile = 0.00006
    truck_capacity = 160000
    maxtime = 0
    timesum=0

    for row in Distribution: ### Iterate through distribution
        supplier = row[0] ### Get Supplier and Demander
        demander = row[1]
        supplyamount = row[2] ### Get Supply Amount
        distance = get_element_by_keys(facilitylist,supplier,demander) ### Get Distance between supplier and demander

        time = int(get_element_by_keys(facilitylist,supplier,demander,element=3)) ### Get Time between supplier and demander
        timesum += time * (supplyamount/truck_capacity)
        if time > maxtime:
            maxtime = time
        costsum += (distance * cost_per_mile * supplyamount) ### Calculate Cost
    return costsum, [maxtime,timesum]


def Iterate(supplypath,demandpath,latlongpath,trials=1,Mtype="Transparent",method="distance"): ### Iterate through trials
    facilitylist = convert_third_item_to_int(read_csv_to_list(join_path("Model/CSVLib/DistanceListShort.csv"))) ### Load Distance List
    costdistribution  = []

    #if type != "Transparent": ### Non-Transparent
        #trials = 1 ### Only 1 trial, unchanged between iterations

    for i in range(trials): ### Iterate through trials
        if i == 0: ### First Trial, fixed facilitylist
            Locations, Distribution = Trial(supplypath,demandpath,latlongpath,facilitylist,i,Mtype=Mtype,method=method)
        else: ### Subsequent Trials, random facilitylist
            Locations, Distribution = Trial(supplypath,demandpath,latlongpath,facilitylist,Mtype=Mtype,method=method)
        cost,time = EvaluateDistribution(Distribution, facilitylist) ### Evaluate Distribution
        costdistribution.append([cost, Distribution, Locations, time]) ### Append to costdistribution
    return costdistribution, Locations


def Minimize(supplypath,demandpath,latlongpath,outputfile,trials=1,Mtype="Transparent",method="distance"): ### Minimize Cost
    costdistribution,Locations = Iterate(supplypath,demandpath,latlongpath,trials=trials,Mtype=Mtype) ### Iterate through trials
    costdistribution = sorted(costdistribution, key=lambda x: x[0]) ### Sort by cost
    df = pd.DataFrame(costdistribution[0][1], columns=['SupplierID', 'DemanderID', 'SupplyAmount']) ### Create distribution DataFrame
    df.to_csv(join_path(outputfile), index=False) ### Save to CSV
    return costdistribution[0], Locations ### Return minimum cost distribution

