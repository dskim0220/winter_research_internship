import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
demand_A1 = 5300
demand_A2 = 4500
demand_A3 = 5400
price_A1 = 124
price_A2 = 109
price_A3 = 115
cost_A1 = 73.30
cost_A2 = 52.90
cost_A3 = 65.40
quota_A1 = 500
quota_A2 = 450
quota_A3 = 550
activation_cost_A1 = 170000
activation_cost_A2 = 150000
activation_cost_A3 = 100000
minimum_batch_A1 = 20
minimum_batch_A2 = 20
minimum_batch_A3 = 16
total_production_limit = 1210

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="x1")
x2 = m.addVar(vtype=GRB.BINARY, name="x2")
x3 = m.addVar(vtype=GRB.BINARY, name="x3")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(price_A1 * x1 + price_A2 * x2 + price_A3 * x3, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 * quota_A1 >= demand_A1, "DemandConstraintA1")
m.addConstr(x2 * quota_A2 >= demand_A2, "DemandConstraintA2")
m.addConstr(x3 * quota_A3 >= demand_A3, "DemandConstraintA3")

m.addConstr(x1 * minimum_batch_A1 >= 20, "MinBatchConstraintA1")
m.addConstr(x2 * minimum_batch_A2 >= 20, "MinBatchConstraintA2")
m.addConstr(x3 * minimum_batch_A3 >= 16, "MinBatchConstraintA3")

m.addConstr(x1 + x2 + x3 <= total_production_limit / 100, "TotalProductionLimit")

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)