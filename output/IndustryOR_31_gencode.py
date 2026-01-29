import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_I = 1.25
price_II = 2.00
price_III = 2.80
raw_material_cost_I = 0.25
raw_material_cost_II = 0.35
raw_material_cost_III = 0.50
fixed_cost_A1 = 321
fixed_cost_A2 = 250
fixed_cost_B1 = 783
fixed_cost_B2 = 200
total_production_I_limit = 1210
total_production_I_and_III_limit = 1510
total_production_II_limit = 800
total_production_I_II_III_limit = 1509

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="x1")
x2 = m.addVar(vtype=GRB.BINARY, name="x2")
x3 = m.addVar(vtype=GRB.BINARY, name="x3")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_I * x1 + price_II * x2 + price_III * x3 - 
    raw_material_cost_I * x1 - raw_material_cost_II * x2 - raw_material_cost_III * x3 - 
    fixed_cost_A1 * x1 + fixed_cost_A2 * x1 - 
    fixed_cost_B1 * x2 + fixed_cost_B2 * x2,
    GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 + x3 <= total_production_I_and_III_limit, "Constraint1")
m.addConstr(x1 + x2 <= total_production_I_II_III_limit, "Constraint2")
m.addConstr(x2 <= total_production_II_limit, "Constraint3")
m.addConstr(x1 <= total_production_I_limit, "Constraint4")
m.addConstr(x3 <= total_production_I_limit, "Constraint5")

# 6. Optimization and Output
m.optimize()
print(f"Optimal Objective Value: {m.objVal}")
for v in m.getVars():
    print(f"{v.varName}: {v.x}")