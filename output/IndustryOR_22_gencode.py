import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 124
price_A2 = 170
price_A3 = 150
min_batch_A1 = 20
min_batch_A2 = 20
min_batch_A3 = 16
max_days = 22

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x_A1 = m.addVar(vtype=GRB.INTEGER, name="x_A1")
x_A2 = m.addVar(vtype=GRB.INTEGER, name="x_A2")
x_A3 = m.addVar(vtype=GRB.INTEGER, name="x_A3")
y_A1 = m.addVar(vtype=GRB.BINARY, name="y_A1")
y_A2 = m.addVar(vtype=GRB.BINARY, name="y_A2")
y_A3 = m.addVar(vtype=GRB.BINARY, name="y_A3")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(price_A1 * x_A1 + price_A2 * x_A2 + price_A3 * x_A3, GRB.MAXIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x_A1 + x_A2 + x_A3 <= max_days * y_A1 * 1210, "R1")  # 1210 tons converted to kg
m.addConstr(x_A1 >= min_batch_A1 * y_A1, "R2")
m.addConstr(x_A1 <= max_days * y_A1, "R3")
m.addConstr(x_A2 >= min_batch_A2 * y_A2, "R4")
m.addConstr(x_A2 <= max_days * y_A2, "R5")
m.addConstr(x_A3 >= min_batch_A3 * y_A3, "R6")
m.addConstr(x_A3 <= max_days * y_A3, "R7")
m.addConstr(y_A1 + y_A2 + y_A3 <= 1, "R8")

# 6. Optimization & Output
m.optimize()
if m.status == GRUBOpy.GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")