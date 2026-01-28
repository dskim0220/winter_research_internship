import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
initial_cost_per_truck_X = 1000
initial_cost_per_truck_Y = 1200
initial_cost_per_truck_Z = 1500
cost_reduction_per_100_investment_X = 10
cost_reduction_per_100_investment_Y = 12
cost_reduction_per_100_investment_Z = 15
total_trucks_available = 50
budget_for_optimization_software = 10000
minimum_trucks_X = 10
minimum_trucks_Y = 15
maximum_trucks_Z = 25
max_cost_reduction_Z = 37500
total_cost_reduction_required = 0
investment_to_savings_ratio = 100 / 75

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
trucks_X = m.addVar(vtype=GRB.CONTINUOUS, name="trucks_X")
trucks_Y = m.addVar(vtype=GRB.CONTINUOUS, name="trucks_Y")
trucks_Z = m.addVar(vtype=GRB.CONTINUOUS, name="trucks_Z")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    initial_cost_per_truck_X * trucks_X + 
    initial_cost_per_truck_Y * trucks_Y + 
    initial_cost_per_truck_Z * trucks_Z - 
    cost_reduction_per_100_investment_X * trucks_X * (trucks_X / 100) - 
    cost_reduction_per_100_investment_Y * trucks_Y * (trucks_Y / 100) - 
    cost_reduction_per_100_investment_Z * trucks_Z * (trucks_Z / 100), 
    GRB.MINIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(trucks_X + trucks_Y + trucks_Z <= total_trucks_available, "total_trucks_constraint")
m.addConstr(trucks_X >= minimum_trucks_X, "minimum_trucks_X_constraint")
m.addConstr(trucks_Y >= minimum_trucks_Y, "minimum_trucks_Y_constraint")

# 6. Optimization and Output
m.optimize()

# Print results for each variable
for v in m.getVars():
    print(f'{v.varName}: {v.x}')
print(f'Total Objective Value: {m.objVal}')