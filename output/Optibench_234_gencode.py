import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_x = 170000
price_y = 124
price_z = 15000
total_trucks = 50
min_x = 10
min_y = 15
max_z = 25
budget_opt = 10000
cost_reduction_ratio = 0.01
total_cost_reduction_z = 37500

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
y_x = m.addVar(vtype=GRB.BINARY, name="y_x")
y_y = m.addVar(vtype=GRB.BINARY, name="y_y")
y_z = m.addVar(vtype=GRB.BINARY, name="y_z")
x_x = m.addVar(vtype=GRB.INTEGER, name="x_x")
x_y = m.addVar(vtype=GRB.INTEGER, name="x_y")
x_z = m.addVar(vtype=GRB.INTEGER, name="x_z")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(price_x * x_x + price_y * x_y + price_z * x_z + total_cost_reduction_z * y_z, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x_x + x_y + x_z == total_trucks, "R1")
m.addConstr(x_x >= min_x * y_x, "R2")
m.addConstr(x_y >= min_y * y_y, "R3")
m.addConstr(x_z <= max_z * y_z, "R4")
m.addConstr(x_z <= total_cost_reduction_z / cost_reduction_ratio, "R5")
m.addConstr(x_x + x_y + x_z >= total_trucks * cost_reduction_ratio, "R6")
m.addConstr(y_z <= budget_opt, "R7")
m.addConstr(x_x + x_y + x_z <= total_trucks, "R8")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")