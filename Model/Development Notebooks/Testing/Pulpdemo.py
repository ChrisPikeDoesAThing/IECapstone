from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Define locations, distances, supply, demand, and truck capacity
locations = ["A", "B", "C"]
distance = {("A", "B"): 10, ("A", "C"): 20, ("B", "C"): 15, ("B", "A"): 10, ("C", "A"): 20, ("C", "B"): 15}
supply = {"A": 50, "B": 0, "C": 0}  # Excess supply at A
demand = {"A": 0, "B": 30, "C": 20}  # Demand at B and C
capacity = 40
fixed_cost = 100
variable_cost = 0.1

# Define the problem
prob = LpProblem("Transportation_Cost_Minimization", LpMinimize)

# Decision variables
trucks = ["T1", "T2"]  # Define a list of trucks
x = LpVariable.dicts("Route", [(i, j, k) for i in locations for j in locations if i != j for k in trucks], 0, 1, cat="Binary")
y = LpVariable.dicts("Units", [(i, j, k) for i in locations for j in locations if i != j for k in trucks], 0, capacity)
z = LpVariable.dicts("TruckUsed", trucks, 0, 1, cat="Binary")

# Objective function
prob += lpSum(fixed_cost * z[k] for k in trucks) + lpSum(variable_cost * distance[(i, j)] * y[(i, j, k)] for i, j in distance for k in trucks)

# Constraints
# Supply constraint
for i in locations:
    prob += lpSum(y[(i, j, k)] for j in locations if i != j for k in trucks) <= supply[i]

# Demand constraint
for j in locations:
    prob += lpSum(y[(i, j, k)] for i in locations if i != j for k in trucks) >= demand[j]

# Truck capacity constraint
for k in trucks:
    prob += lpSum(y[(i, j, k)] for i, j in distance) <= capacity * z[k]

# Flow conservation constraint
for k in trucks:
    for i in locations:
        prob += lpSum(y[(j, i, k)] for j in locations if j != i) == lpSum(y[(i, j, k)] for j in locations if j != i)

# Routing constraints
for k in trucks:
    for i, j in distance:
        prob += x[(i, j, k)] <= y[(i, j, k)]

# Solve the problem
prob.solve()

# Print results
print("Status:", prob.status)
for i, j in distance:
    for k in trucks:
        if x[(i, j, k)].varValue > 0:
            print(f"Truck {k} on route {i} -> {j}: {y[(i, j, k)].varValue} units")
            