import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
smartphones_per_hour_1 = 10
tablets_per_hour_1 = 5
laptops_per_hour_1 = 3
smartphones_per_hour_2 = 8
tablets_per_hour_2 = 6
laptops_per_hour_2 = 4
smartphones_per_hour_3 = 6
tablets_per_hour_3 = 7
laptops_per_hour_3 = 5
smartphones_per_hour_4 = 5
tablets_per_hour_4 = 8
demand_smartphones = 1210
demand_tablets = 1090
demand_laptops = 800

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
y1 = m.addVar(vtype=GRB.BINARY, name="y1")
y2 = m.addVar(vtype=GRB.BINARY, name="y2")
y3 = m.addVar(vtype=GRB.BINARY, name="y3")
y4 = m.addVar(vtype=GRB.BINARY, name="y4")
x11 = m.addVar(vtype=GRB.INTEGER, name="x11")
x12 = m.addVar(vtype=GRB.INTEGER, name="x12")
x13 = m.addVar(vtype=GRB.INTEGER, name="x13")
x21 = m.addVar(vtype=GRB.INTEGER, name="x21")
x22 = m.addVar(vtype=GRB.INTEGER, name="x22")
x23 = m.addVar(vtype=GRB.INTEGER, name="x23")
x31 = m.addVar(vtype=GRB.INTEGER, name="x31")
x32 = m.addVar(vtype=GRB.INTEGER, name="x32")
x33 = m.addVar(vtype=GRB.INTEGER, name="x33")
x41 = m.addVar(vtype=GRB.INTEGER, name="x41")
x42 = m.addVar(vtype=GRB.INTEGER, name="x42")
x43 = m.addVar(vtype=GRB.INTEGER, name="x43")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    smartphones_per_hour_1 * x11 + smartphones_per_hour_2 * x21 + smartphones_per_hour_3 * x31 + smartphones_per_hour_4 * x41,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x11 + x21 + x31 + x41 <= demand_smartphones, "smartphones_constraint")
m.addConstr(x12 + x22 + x32 + x42 <= demand_tablets, "tablets_constraint")
m.addConstr(x13 + x23 + x33 + x43 <= demand_laptops, "laptops_constraint")

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)