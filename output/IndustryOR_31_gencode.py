import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_I = 1.25
price_II = 2.00
price_III = 2.80
raw_material_cost_I = 0.25
raw_material_cost_II = 0.35
raw_material_cost_III = 0.50
machine_hours_A1 = 10000
machine_hours_A2 = 4000
machine_hours_B1 = 7000
machine_hours_B2 = 4000
machine_hours_B3 = 0
full_capacity_cost_A1 = 321
full_capacity_cost_A2 = 250
full_capacity_cost_B1 = 783
full_capacity_cost_B2 = 200
total_production_limit = 1509
production_limit_I = 1200
production_limit_III = 1510
production_limit_II = 800

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(name="Production_I", obj=price_I, vtype=GRB.CONTINUOUS, lb=0, ub=production_limit_I)
x2 = m.addVar(name="Production_II", obj=price_II, vtype=GRB.CONTINUOUS, lb=0, ub=production_limit_II)
x3 = m.addVar(name="Production_III", obj=price_III, vtype=GRB.CONTINUOUS, lb=0, ub=production_limit_III)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(x1 * price_I + x2 * price_II + x3 * price_III, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 + x2 + x3 <= total_production_limit, "Total_Production_Limit")
m.addConstr(x1 <= production_limit_I, "Production_I_Limit")
m.addConstr(x3 <= production_limit_III, "Production_III_Limit")

# 6. Optimization and Output
m.optimize()
print(f"Optimal Solution:")
for v in m.getVars():
    print(f"{v.varName}: {v.x}")
print(f"Optimal Objective Value: {m.objVal}")