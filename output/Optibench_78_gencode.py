import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_NY = 400
price_LA = 500
price_CH = 300
price_AT = 150
shipping_NY_R1 = 20
shipping_NY_R2 = 40
shipping_NY_R3 = 50
shipping_LA_R1 = 48
shipping_LA_R2 = 15
shipping_LA_R3 = 26
shipping_CH_R1 = 26
shipping_CH_R2 = 35
shipping_CH_R3 = 18
shipping_AT_R1 = 24
shipping_AT_R2 = 50
shipping_AT_R3 = 35
demand_R1 = 80
demand_R2 = 70
demand_R3 = 40

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="Open_New_York")
x2 = m.addVar(vtype=GRB.BINARY, name="Open_Los_Angeles")
x3 = m.addVar(vtype=GRB.BINARY, name="Open_Chicago")
x4 = m.addVar(vtype=GRB.BINARY, name="Open_Atlanta")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_NY * x1 + price_LA * x2 + price_CH * x3 + price_AT * x4,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr((x1 * shipping_NY_R1 + x2 * shipping_LA_R1 + x3 * shipping_CH_R1 + x4 * shipping_AT_R1) == demand_R1, "Supply_R1")
m.addConstr((x1 * shipping_NY_R2 + x2 * shipping_LA_R2 + x3 * shipping_CH_R2 + x4 * shipping_AT_R2) == demand_R2, "Supply_R2")
m.addConstr((x1 * shipping_NY_R3 + x2 * shipping_LA_R3 + x3 * shipping_CH_R3 + x4 * shipping_AT_R3) == demand_R3, "Supply_R3")

# 6. Optimization and Output
m.optimize()
print(f"Optimal Objective Value: {m.objVal}")
for v in m.getVars():
    print(f"{v.varName}: {v.x}")