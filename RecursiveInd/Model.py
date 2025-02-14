
import os
import numpy as np
import random
import csv
import pandas as pd

def join_path(filename):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory
    parent_dir = os.path.dirname(current_dir)

    # Construct the path to the file in the parent directory
    file_path = os.path.join(parent_dir, filename)
    return file_path

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







def find_optimal_distribution_with_trucks(facilitylist, supply, demand, cost_per_mile, truck_capacity, iterations=100):
    def allocate_supply(facilitylist, supply_dict, demand_dict, trucks_dict, cost_per_mile, truck_capacity):
        # Create a list to store supply distribution
        supply_distribution = []

        # Sort the facility list by cost
        facilitylist.sort(key=lambda x: float(x[2]) * cost_per_mile)

        # Allocate supply to demanders starting with the lowest cost
        for facility in facilitylist:
            supplier_id = facility[0]
            demander_id = facility[1]
            cost = float(facility[2]) * cost_per_mile

            if supplier_id in supply_dict and demander_id in demand_dict:
                supplier_supply = supply_dict[supplier_id]
                demander_demand = demand_dict[demander_id]
                available_trucks = trucks_dict[supplier_id]

                if supplier_supply > 0 and demander_demand > 0 and available_trucks > 0:
                    # Calculate the number of trucks needed for the allocation
                    trucks_needed = int(np.ceil(min(supplier_supply, demander_demand) / truck_capacity))
                    allocated_supply = min(supplier_supply, demander_demand, trucks_needed * truck_capacity)

                    supply_distribution.append([supplier_id, demander_id, allocated_supply, cost])

                    supply_dict[supplier_id] -= allocated_supply
                    demand_dict[demander_id] -= allocated_supply
                    trucks_dict[supplier_id] -= trucks_needed

        return supply_distribution

    best_distribution = None
    best_cost = float('inf')

    for _ in range(iterations):
        # Shuffle the facility list to start with a different order
        random.shuffle(facilitylist)

        # Create dictionaries for quick access
        supply_dict = {row[0]: int(float(row[2])) for row in supply}
        trucks_dict = {row[0]: int(float(row[3])) if len(row) > 3 else float('inf') for row in supply}
        demand_dict = {row[0]: int(float(row[2])) for row in demand}

        # Allocate supply
        supply_distribution = allocate_supply(facilitylist, supply_dict, demand_dict, trucks_dict, cost_per_mile, truck_capacity)

        # Calculate the total cost
        total_cost = sum(row[3] for row in supply_distribution)

        # Update the best solution if the current one is better
        if total_cost < best_cost:
            best_cost = total_cost
            best_distribution = supply_distribution

    # Create the supply distribution DataFrame
    df_supply_distribution = pd.DataFrame(best_distribution, columns=['SupplierID', 'DemanderID', 'SupplyAmount', 'Cost'])
    return df_supply_distribution

facilitylist = read_csv_to_list(join_path("Model/CSVLib/DistanceListShort.csv"))
facilitylist = sort_by_distance_list(facilitylist)


#Scale Supply for 1 week
supply = scale_supply(read_csv_to_list(join_path("Model/CSVLib/SupplierData.csv")), 1/52)
demand = read_csv_to_list(join_path("Model/CSVLib/CountyData.csv"))

correlated_demand, df1 = fill_demand_correlation(facilitylist, supply, demand)
competition_demand, df2 = fill_demand_competition(facilitylist, supply, demand)

df1.to_csv(join_path("Model/CSVLib/SupplyDistributionCorrelation.csv"), index=False)
df2.to_csv(join_path("Model/CSVLib/SupplyDistributionCompetition.csv"), index=False)
save_demand_to_csv(correlated_demand, join_path("Model/CSVLib/CountyDataCorrelation.csv"))
save_demand_to_csv(competition_demand, join_path("Model/CSVLib/CountyDataCompetition.csv"))

cost_per_mile = 1.0  # Example cost per mile
truck_capacity = 160000  # Example truck capacity

df_optimal_distribution = find_optimal_distribution_with_trucks(facilitylist, supply, demand, cost_per_mile, truck_capacity)
if df_optimal_distribution is not None:
    df_optimal_distribution.to_csv(join_path("Model/CSVLib/OptimalSupplyDistributionWithTrucks.csv"), index=False)












def initialize_population(facilitylist, supply, demand, population_size):
    population = []
    for _ in range(population_size):
        random.shuffle(facilitylist)
        population.append(facilitylist.copy())
    return population

def calculate_fitness(solution, supply, demand, cost_per_mile, truck_capacity):
    supply_dict = {row[0]: int(float(row[2])) for row in supply}
    trucks_dict = {row[0]: int(float(row[3])) if len(row) > 3 else float('inf') for row in supply}
    demand_dict = {row[0]: int(float(row[2])) for row in demand}
    total_cost = 0
    for facility in solution:
        supplier_id = facility[0]
        demander_id = facility[1]
        cost = float(facility[2]) * cost_per_mile
        if supplier_id in supply_dict and demander_id in demand_dict:
            supplier_supply = supply_dict[supplier_id]
            demander_demand = demand_dict[demander_id]
            available_trucks = trucks_dict[supplier_id]
            if supplier_supply > 0 and demander_demand > 0 and available_trucks > 0:
                trucks_needed = int(np.ceil(min(supplier_supply, demander_demand) / truck_capacity))
                allocated_supply = min(supplier_supply, demander_demand, trucks_needed * truck_capacity)
                total_cost += cost * allocated_supply
                supply_dict[supplier_id] -= allocated_supply
                demand_dict[demander_id] -= allocated_supply
                trucks_dict[supplier_id] -= trucks_needed
    return total_cost

def selection(population, fitnesses, num_parents):
    parents = np.random.choice(population, size=num_parents, p=fitnesses/fitnesses.sum(), replace=False)
    return parents

def crossover(parents, population_size):
    offspring = []
    for _ in range(population_size):
        parent1, parent2 = random.sample(list(parents), 2)
        crossover_point = random.randint(0, len(parent1))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        offspring.append(child)
    return offspring

def mutation(offspring, mutation_rate):
    for child in offspring:
        if random.random() < mutation_rate:
            swap_idx1, swap_idx2 = random.sample(range(len(child)), 2)
            child[swap_idx1], child[swap_idx2] = child[swap_idx2], child[swap_idx1]
    return offspring

def genetic_algorithm(facilitylist, supply, demand, cost_per_mile, truck_capacity, population_size=50, generations=100, mutation_rate=0.1):
    population = initialize_population(facilitylist, supply, demand, population_size)
    best_solution = None
    best_fitness = float('inf')
    for generation in range(generations):
        fitnesses = np.array([calculate_fitness(solution, supply, demand, cost_per_mile, truck_capacity) for solution in population])
        best_idx = np.argmin(fitnesses)
        if fitnesses[best_idx] < best_fitness:
            best_fitness = fitnesses[best_idx]
            best_solution = population[best_idx]
        parents = selection(population, fitnesses, population_size // 2)
        offspring = crossover(parents, population_size)
        population = mutation(offspring, mutation_rate)
    return best_solution, best_fitness

best_solution, best_fitness = genetic_algorithm(facilitylist, supply, demand, cost_per_mile, truck_capacity, population_size=50, generations=100, mutation_rate=0.1)

# Create the supply distribution DataFrame
supply_distribution = []
supply_dict = {row[0]: int(float(row[2])) for row in supply}
trucks_dict = {row[0]: int(float(row[3])) if len(row) > 3 else float('inf') for row in supply}
demand_dict = {row[0]: int(float(row[2])) for row in demand}
for facility in best_solution:
    supplier_id = facility[0]
    demander_id = facility[1]
    cost = float(facility[2]) * cost_per_mile
    if supplier_id in supply_dict and demander_id in demand_dict:
        supplier_supply = supply_dict[supplier_id]
        demander_demand = demand_dict[demander_id]
        available_trucks = trucks_dict[supplier_id]
        if supplier_supply > 0 and demander_demand > 0 and available_trucks > 0:
            trucks_needed = int(np.ceil(min(supplier_supply, demander_demand) / truck_capacity))
            allocated_supply = min(supplier_supply, demander_demand, trucks_needed * truck_capacity)
            supply_distribution.append([supplier_id, demander_id, allocated_supply, cost])
            supply_dict[supplier_id] -= allocated_supply
            demand_dict[demander_id] -= allocated_supply
            trucks_dict[supplier_id] -= trucks_needed

df_supply_distribution = pd.DataFrame(supply_distribution, columns=['SupplierID', 'DemanderID', 'SupplyAmount', 'Cost'])
df_supply_distribution.to_csv("Model/CSVLib/OptimalSupplyDistributionWithTrucks.csv", index=False)