
import os
import numpy as np

def join_path(filename):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to the file in the parent directory
    file_path = os.path.join(parent_dir, filename)
    return file_path




import csv
def read_csv_to_list(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def remove_rows_list(data):
    return [row for row in data if int(row[0]) > 25]

def sort_by_distance_list(data):
    from collections import defaultdict
    # Group rows by ID1
    grouped_data = defaultdict(list)
    for row in data:
        grouped_data[row[0]].append(row)
    # Sort each group by DISTANCE
    sorted_data = []
    for key in grouped_data:
        sorted_group = sorted(grouped_data[key], key=lambda x: float(x[2]))
        sorted_data.extend(sorted_group)

    return sorted_data

def scale_supply(supply_list, scalar):
    for row in supply_list:
        row[2] = str(int(row[2]) * scalar)
    return supply_list

def sum_total_supply(supply_list):
    total_supply = sum(int(float(row[2])) for row in supply_list)
    return total_supply

def sum_total_demand(demand_list):
    total_demand = sum(int(float(row[2])) for row in demand_list)
    return total_demand



def read_csv_to_dict_list(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def remove_rows_dict_list(data):
    return [row for row in data if int(row['ID1']) > 25]


def sort_by_distance_dict_list(data):
    from collections import defaultdict

    # Group rows by ID1
    grouped_data = defaultdict(list)
    for row in data:
        grouped_data[row['ID1']].append(row)

    # Sort each group by DISTANCE
    sorted_data = []
    for key in grouped_data:
        sorted_group = sorted(grouped_data[key], key=lambda x: float(x['DISTANCE']))
        sorted_data.extend(sorted_group)

    return sorted_data




import pandas as pd
def read_csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df

def remove_rows_dataframe(df):
    return df[df['ID1'] > 25]

def sort_by_distance_dataframe(df):
    return df.sort_values(by=['ID1', 'DISTANCE'])

def save_demand_to_csv(demand, file_path):
    # Create a DataFrame from the demand list
    df_demand = pd.DataFrame(demand, columns=['DemanderID', 'Name', 'DemandAmount'])
    
    # Save the DataFrame to a CSV file
    df_demand.to_csv(file_path, index=False)
    return


def fill_demand_correlation(facilitylist, supply, demand):
    # Create a dictionary to store remaining demand
    remaining_demand = {row[0]: int(float(row[2])) for row in demand}
    
    # Create a list to store supply distribution
    supply_distribution = []

    # Iterate through the supply list
    for supplier in supply:
        supplier_id = supplier[0]
        supplier_supply = int(float(supplier[2]))
        
        # Find the corresponding rows in the facility list
        for facility in facilitylist:
            if facility[0] == supplier_id:
                demander_id = facility[1]
                if demander_id in remaining_demand:
                    demander_demand = remaining_demand[demander_id]
                    if supplier_supply >= demander_demand:
                        supply_distribution.append([supplier_id, demander_id, demander_demand])
                        supplier_supply -= demander_demand
                        remaining_demand[demander_id] = 0
                    else:
                        supply_distribution.append([supplier_id, demander_id, supplier_supply])
                        remaining_demand[demander_id] -= supplier_supply
                        supplier_supply = 0
                    if supplier_supply == 0:
                        break
    
    # Update the demand list with the remaining demand
    for row in demand:
        row[2] = max(remaining_demand[row[0]], 0)
    
    # Create a DataFrame from the supply distribution
    df_supply_distribution = pd.DataFrame(supply_distribution, columns=['SupplierID', 'DemanderID', 'SupplyAmount'])
    
    return demand, df_supply_distribution


def fill_demand_competition(facilitylist, supply, demand):
    # Create a dictionary to store remaining demand
    remaining_demand = {row[0]: int(float(row[2])) for row in demand}
    
    # Create a list to store supply distribution
    supply_distribution = []

    # Iterate through the supply list
    for supplier in supply:
        supplier_id = supplier[0]
        supplier_supply = int(float(supplier[2]))
        
        # Find the corresponding rows in the facility list
        for facility in facilitylist:
            if facility[0] == supplier_id:
                demander_id = facility[1]
                if demander_id in remaining_demand:
                    demander_demand = remaining_demand[demander_id]
                    supply_distribution.append([supplier_id, demander_id, supplier_supply])
                    remaining_demand[demander_id] -= supplier_supply
                    supplier_supply = 0
                    if supplier_supply == 0:
                        break
    
    # Update the demand list with the remaining demand
    for row in demand:
        row[2] = remaining_demand[row[0]]
    
    # Create a DataFrame from the supply distribution
    df_supply_distribution = pd.DataFrame(supply_distribution, columns=['SupplierID', 'DemanderID', 'SupplyAmount'])
    
    return demand, df_supply_distribution

def find_optimal_distribution_greedy(facilitylist, supply, demand):
    # Create dictionaries for quick access
    supply_dict = {row[0]: int(float(row[2])) for row in supply}
    demand_dict = {row[0]: int(float(row[2])) for row in demand}

    # Create a list of unique suppliers and demanders
    suppliers = list(supply_dict.keys())
    demanders = list(demand_dict.keys())

    # Create the cost matrix
    cost_matrix = np.zeros((len(suppliers), len(demanders)))
    for facility in facilitylist:
        supplier_id = facility[0]
        demander_id = facility[1]
        distance = float(facility[2])
        if supplier_id in suppliers and demander_id in demanders:
            i = suppliers.index(supplier_id)
            j = demanders.index(demander_id)
            cost_matrix[i, j] = distance

    # Create a list to store supply distribution
    supply_distribution = []

    # Sort the facility list by distance
    facilitylist.sort(key=lambda x: float(x[2]))

    # Allocate supply to demanders starting with the closest ones
    for facility in facilitylist:
        supplier_id = facility[0]
        demander_id = facility[1]
        distance = float(facility[2])

        if supplier_id in supply_dict and demander_id in demand_dict:
            supplier_supply = supply_dict[supplier_id]
            demander_demand = demand_dict[demander_id]

            if supplier_supply > 0 and demander_demand > 0:
                allocated_supply = min(supplier_supply, demander_demand)
                supply_distribution.append([supplier_id, demander_id, allocated_supply, distance])

                supply_dict[supplier_id] -= allocated_supply
                demand_dict[demander_id] -= allocated_supply

    # Create the supply distribution DataFrame
    df_supply_distribution = pd.DataFrame(supply_distribution, columns=['SupplierID', 'DemanderID', 'SupplyAmount', 'Distance'])
    return df_supply_distribution


# Example usage
facilitylist = read_csv_to_list(join_path("Model/CSVLib/DistanceListShort.csv"))
facilitylist = sort_by_distance_list(facilitylist)

supply = scale_supply(read_csv_to_list(join_path("Model/CSVLib/SupplierData.csv")), 1/52)
demand = read_csv_to_list(join_path("Model/CSVLib/CountyData.csv"))

print(f" The Total Supply is {sum_total_supply(supply)}")
print(f" The Total Demand is {sum_total_demand(demand)}")

correlated_demand, df1 = fill_demand_correlation(facilitylist, supply, demand)
competition_demand, df2 = fill_demand_competition(facilitylist, supply, demand)

df1.to_csv(join_path("Model/CSVLib/SupplyDistributionCorrelation.csv"), index=False)
df2.to_csv(join_path("Model/CSVLib/SupplyDistributionCompetition.csv"), index=False)
save_demand_to_csv(correlated_demand, join_path("Model/CSVLib/CountyDataCorrelation.csv"))
save_demand_to_csv(competition_demand, join_path("Model/CSVLib/CountyDataCompetition.csv"))

df_optimal_distribution = find_optimal_distribution_greedy(facilitylist, supply, demand)
if df_optimal_distribution is not None:
    df_optimal_distribution.to_csv(join_path("Model/CSVLib/OptimalSupplyDistributionGreedy.csv"), index=False)