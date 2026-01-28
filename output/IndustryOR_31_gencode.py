import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_I = 1.25
price_II = 2.00
price_III = 2.80
raw_material_cost_I = 0.25
raw_material_cost_II = 0.35
raw_material_cost_III = 0.50
time_I_A1 = 5
time_I_A2 = 7
time_I_B1 = 6
time_I_B2 = 4
time_I_B3 = 7
time_II_A1 = 10
time_II_A2 = 9
time_II_B1 = 8
time_II_B2 = 0
time_II_B3 = 0
time_III_A1 = 0
time_III_A2 = 12
time_III_B1 = 11
time_III_B2 = 11
time_III_B3 = 0
capacity_A1 = 10000
capacity_A2 = 4000
capacity_B1 = 7000
capacity_B2 = 4000
capacity_B3 = 0
fixed_cost_A1 = 321
fixed_cost_A2 = 250
fixed_cost_B1 = 783
fixed_cost_B2 = 200
fixed_cost_B3 = 0

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="x1")
x2 = m.addVar(vtype=GRB.BINARY, name="x2")
x3 = m.addVar(vtype=GRB.BINARY, name="x3")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_I * x1 + price_II * x2 + price_III * x3,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 * time_I_A1 + x2 * time_II_A1 + x3 * time_III_A1 <= capacity_A1, "constraint_A1")
m.addConstr(x1 * time_I_A2 + x2 * time_II_A2 + x3 * time_III_A2 <= capacity_A2, "constraint_A2")
m.addConstr(x1 * time_I_B1 + x2 * time_II_B1 + x3 * time_III_B1 <= capacity_B1, "constraint_B1")
m.addConstr(x1 * time_I_B2 + x2 * time_II_B2 + x3 * time_III_B2 <= capacity_B2, "constraint_B2")
m.addConstr(x1 * time_I_B3 + x2 * time_II_B3 + x3 * time_III_B3 <= capacity_B3, "constraint_B3")

# 6. Optimization and Output
m.optimize()
print(f"Optimal objective value: {m.objVal}")
for v in m.getVars():
    print(f"{v.varName} = {v.x}")