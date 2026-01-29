import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
bandwidth_AB = 90
bandwidth_AD = 67
bandwidth_AE_direct = 65
bandwidth_BE_direct = 34
bandwidth_CD = 25
bandwidth_CE = 80
sum_bandwidth = 100
transmission_efficiency_AE = 0.90
transmission_efficiency_DE = 0.96
transmission_efficiency_AB = 0.90

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
y_AC = m.addVar(vtype=GRB.BINARY, name="y_AC")
y_AD = m.addVar(vtype=GRB.BINARY, name="y_AD")
y_AE = m.addVar(vtype=GRB.BINARY, name="y_AE")
x_AC = m.addVar(vtype=GRB.INTEGER, name="x_AC")
x_AD = m.addVar(vtype=GRB.INTEGER, name="x_AD")
x_AE = m.addVar(vtype=GRB.INTEGER, name="x_AE")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(x_AC + x_AD + x_AE, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
# Ensure unit consistency (e.g., 1,210 tons -> 12100 in 100kg units)
m.addConstr(x_AC + x_AD + x_AE >= sum_bandwidth, "sum_bandwidth_constraint")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Total objective value = {m.objVal}')