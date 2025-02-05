import csv

def csv_to_dict(csv_file):
    data_dict = {}
    id_list = []
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            #print(row)
            data_dict[row[0]] = int(float(row[2]))  # Convert QTY to integer if needed
            id_list.append(row[0])
    
    return data_dict, id_list

def csv_to_distance_dict(csv_file):
    distance_dict = {}
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            key = (row[0], row[1])
            distance_dict[key] = float(row[2])  # Convert Distance to float if needed
    
    return distance_dict




import pyomo.environ as pyo

supply, suppliers = csv_to_dict('SupplierData.csv')
demand, counties = csv_to_dict('CountyData.csv')

#print(counties)
# Distance matrix (distance from supplier to county)
distance = csv_to_distance_dict("DistanceList.csv")
#print(distance)
# Truck capacity
truck_capacity = 16000

# Cost per unit-mile
cost_per_unit_mile = .156

# Create the Pyomo model
model = pyo.ConcreteModel()

# Define sets
model.suppliers = pyo.Set(initialize=suppliers)
model.counties = pyo.Set(initialize=counties)

# Define parameters
model.supply = pyo.Param(model.suppliers, initialize=supply)
model.demand = pyo.Param(model.counties, initialize=demand)
model.distance = pyo.Param(model.suppliers, model.counties, initialize=distance)
model.truck_capacity = pyo.Param(initialize=truck_capacity)
model.cost_per_unit_mile = pyo.Param(initialize=cost_per_unit_mile)

# Define decision variables
model.x = pyo.Var(model.suppliers, model.counties, domain=pyo.NonNegativeReals)  # Amount shipped from supplier to county
model.trucks = pyo.Var(model.suppliers, model.counties, domain=pyo.NonNegativeIntegers)  # Number of trucks used

# Objective: Minimize total cost
def total_cost_rule(model):
    return sum(
        model.cost_per_unit_mile * model.distance[s, c] * model.x[s, c]
        for s in model.suppliers
        for c in model.counties
    )

model.total_cost = pyo.Objective(rule=total_cost_rule, sense=pyo.minimize)

# Constraints
# 1. Supply constraint: Total shipped from each supplier <= supply
def supply_constraint_rule(model, s):
    return sum(model.x[s, c] for c in model.counties) <= model.supply[s]

model.supply_constraint = pyo.Constraint(model.suppliers, rule=supply_constraint_rule)

# 2. Demand constraint: Total shipped to each county >= demand
def demand_constraint_rule(model, c):
    return sum(model.x[s, c] for s in model.suppliers) >= model.demand[c]

model.demand_constraint = pyo.Constraint(model.counties, rule=demand_constraint_rule)

# 3. Truck capacity constraint: Amount shipped <= number of trucks * truck capacity
def truck_capacity_constraint_rule(model, s, c):
    return model.x[s, c] <= model.trucks[s, c] * model.truck_capacity

model.truck_capacity_constraint = pyo.Constraint(model.suppliers, model.counties, rule=truck_capacity_constraint_rule)

# Solve the model
solver = pyo.SolverFactory('gurobi')  # Use GLPK solver (open-source)
results = solver.solve(model)

# Print results
print("Objective Value (Total Cost):", pyo.value(model.total_cost))
print("\nShipments:")
for s in model.suppliers:
    for c in model.counties:
        if pyo.value(model.x[s, c]) > 0:
            print(f"Ship {pyo.value(model.x[s, c]):.2f} units from {s} to {c} using {pyo.value(model.trucks[s, c])} trucks")