import csv
import os
import pandas as pd

def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

def csv_to_dict_list(csv_file_path, has_headers=0):

    dict_list = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        if has_headers:
            headers = next(csv_reader)
        else:
            headers = [str(i) for i in range(len(next(csv_reader)))]
            file.seek(0)
        for row in csv_reader:
            row_dict = {i: row[i] for i in range(len(headers))}
            dict_list.append(row_dict)
    return dict_list

def find_demand_difference(Original, Updated, output_path):
    input1 = csv_to_dict_list(Original, has_headers=1)
    input2 = csv_to_dict_list(Updated, has_headers=0)
    
    demand_diff = []
    
    for original in input1:
        for updated in input2:
            if original[0] == updated[0]:
                if float(original[2]) == 0:
                    diff = 0
                else:
                    diff = round((float(original[2])-(float(updated[2]))))
                demand_diff.append([original[0], original[1], diff])
                break
    
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'County', 'Demand Difference'])
        for row in demand_diff:
            writer.writerow(row)

def find_demand_fill(inputpath1, inputpath2, output_path):
    input1 = csv_to_dict_list(inputpath1, has_headers=1)
    input2 = csv_to_dict_list(inputpath2, has_headers=0)
    
    demand_diff = []
    
    for original in input1:
        for updated in input2:
            if original[0] == updated[0]:
                if float(original[2]) == 0:
                    diff = 0
                else:
                    diff = round((float(original[2])-(float(updated[2]))) / float(original[2]), 3)
                demand_diff.append([original[0], original[1], diff])
                break
    
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'County', 'Demand Fill'])
        for row in demand_diff:
            writer.writerow(row)

# Example usage
def find_fill_and_difference(Original, Updated, outputpath1,outputpath2):
    OriginalDemand = join_path(Original)
    UpdatedDemand = join_path(Updated)

   #
   #  find_differences_in_demand(OriginalDemand, UpdatedDemand, join_path(outputpath1))
    find_demand_fill(OriginalDemand, UpdatedDemand, join_path(outputpath1))
    find_demand_difference(OriginalDemand, UpdatedDemand, join_path(outputpath2))

def analyze_csv_files(transparent_demand_path,transparent_demand_difference_path, non_transparent_demand_path, non_transparent_demand_difference_path,county_data_path):
 
    # Read the CSV files
    transparent_demand = pd.read_csv(join_path(transparent_demand_path))
    non_transparent_demand = pd.read_csv(join_path(non_transparent_demand_path))
    
    county_data = pd.read_csv(join_path(county_data_path))
    
    # Perform analysis
    county_data['Transparent Fairness'] =  (county_data['DEMAND'] - transparent_demand['Updated Demand'])/ county_data['DEMAND'] 
    county_data['Non-Transparent Fairness'] =  (county_data['DEMAND'] - non_transparent_demand['Updated Demand'])/ county_data['DEMAND']
    county_data.to_csv(join_path('Model/CSVResults/Analysis.csv'))
    
    # Calculate average and standard deviation
    avg_transparent_fairness = county_data['Transparent Fairness'].mean()
    print(avg_transparent_fairness)
    std_transparent_fairness = county_data['Transparent Fairness'].std()
    avg_non_transparent_fairness = county_data['Non-Transparent Fairness'].mean()
    std_non_transparent_fairness = county_data['Non-Transparent Fairness'].std()
    
    transparentresults = [avg_transparent_fairness, std_transparent_fairness]
    nontransparentresults = [avg_non_transparent_fairness, std_non_transparent_fairness]
  
    return(transparentresults, nontransparentresults)

def find_ratio(county_supply_path, supplier_demand_path):
    """
    Find the ratio of the sum of County Supply to Supplier Demand.
    
    :param county_supply_path: Path to the County Supply CSV file
    :param supplier_demand_path: Path to the Supplier Demand CSV file
    :return: Ratio of the sum of County Supply to Supplier Demand
    """
    county_supply = pd.read_csv(join_path(county_supply_path))
    supplier_demand = pd.read_csv(join_path(supplier_demand_path))
    
    total_county_supply = county_supply['SUPPLY'].sum()
    total_supplier_demand = supplier_demand['DEMAND'].sum()
    
    ratio = total_county_supply / total_supplier_demand
    return ratio