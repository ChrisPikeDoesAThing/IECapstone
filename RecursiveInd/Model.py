
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

# Example usage

def fill_demand(facilitylist, supply, demand):
    # Create a dictionary for quick access to demand by ID2
    demand_dict = {row[0]: row for row in demand}
    
    # Create a dictionary to store remaining demand
    remaining_demand = {row[0]: int(row[2]) for row in demand}
    
    # Iterate through the supply list
    for supplier in supply:
        supplier_id = supplier[0]
        supplier_supply = int(supplier[2])
        
        # Find the corresponding rows in the facility list
        for facility in facilitylist:
            print (facility)
            if facility[0] == supplier_id:
                demander_id = facility[1]
                if demander_id in remaining_demand:
                    demander_demand = remaining_demand[demander_id]
                    if supplier_supply >= demander_demand:
                        supplier_supply -= demander_demand
                        remaining_demand[demander_id] = 0
                    else:
                        remaining_demand[demander_id] -= supplier_supply
                        supplier_supply = 0
                    if supplier_supply == 0:
                        break
    
    # Update the demand list with the remaining demand
    for row in demand:
        row[2] = remaining_demand[row[0]]
    
    return demand

# Example usage
facilitylist = read_csv_to_list("Model/CSVLib/DistanceListShort.csv")
facilitylist = sort_by_distance_list(facilitylist)

supply = read_csv_to_list("Model/CSVLib/Supply.csv")
demand = read_csv_to_list("Model/CSVLib/Demand.csv")

updated_demand = fill_demand(facilitylist, supply, demand)
print(updated_demand)




def FindOptimalDist():

    facilitylist = read_csv_to_list("Model\CSVLib\DistanceListShort.csv")
    facilitylist = sort_by_distance_list(remove_rows_list(facilitylist))

    supply = read_csv_to_list("Model\CSVLib\SupplierData.csv")
    demand = read_csv_to_list("Model\CSVLib\CountyData.csv")
        #Fill Demand Starting with Cheapest.



