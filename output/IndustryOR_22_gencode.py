import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_A1 = 124
price_A2 = 109
price_A3 = 170000 / 100  # Convert tons to 100kg units
demand_A1 = 5300
demand_A2 = 4800
demand_A3 = 1210000 / 100  # Convert tons to 100kg units
activation_cost_A1 = 1000
activation_cost_A2 = 1500
activation_cost_A3 = 2000
min_batch_A1 = 100
min_batch_A2 = 150
min_batch_A3 = 200
total_production_limit = 1210000 / 100  # Convert tons to 100kg units
activation_time_A1 = 57

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
produce_A1 = m.addVar(vtype=GRB.BINARY, name="produce_A1")
produce_A2 = m.addVar(vtype=GRB.BINARY, name="produce_A2")
produce_A3 = m.addVar(vtype=GRB.BINARY, name="produce_A3")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_A1 * produce_A1 + price_A2 * produce_A2 + price_A3 * produce_A3,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(demand_A1 * produce_A1 + demand_A2 * produce_A2 + demand_A3 * produce_A3 <= total_production_limit, "Total_Production_Limit")
m.addConstr(activation_time_A1 * produce_A1 >= activation_time_A1, "Activation_Time_Constraint")
m.addConstr(activation_cost_A1 * produce_A1 + activation_cost_A2 * produce_A2 + activation_cost_A3 * produce_A3 >= 0, "Fixed_Activation_Costs")
m.addConstr(min_batch_A1 <= produce_A1, "Minimum_Batch_Constraint_A1")
m.addConstr(min_batch_A2 <= produce_A2, "Minimum_Batch_Constraint_A2")
m.addConstr(min_batch_A3 <= produce_A3, "Minimum_Batch_Constraint_A3")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Total Objective Value = {m.objVal}')