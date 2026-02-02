import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A = 120
price_B = 110
price_C = 100
cost_A = 30000
cost_B = 25000
cost_C = 20000
limit_tables = 600
min_tables = 150
min_order_A = 30

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
y_A = m.addVar(vtype=GRB.BINARY, name="y_A")
y_B = m.addVar(vtype=GRB.BINARY, name="y_B")
y_C = m.addVar(vtype=GRB.BINARY, name="y_C")
x_A = m.addVar(vtype=GRB.INTEGER, name="x_A")
x_B = m.addVar(vtype=GRB.INTEGER, name="x_B")
x_C = m.addVar(vtype=GRB.INTEGER, name="x_C")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(x_A*price_A + x_B*price_B + x_C*price_C, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(y_A + y_B + y_C >= 1, "R1")
m.addConstr(x_A + x_B + x_C >= min_tables, "R2")
m.addConstr(x_A + x_B + x_C <= limit_tables, "R3")
m.addConstr(x_A >= min_order_A * y_B, "R4")
m.addConstr(x_B >= x_B + x_C, "R5")
m.addConstr(x_A + x_B >= 25, "R6")
m.addConstr(x_B + x_C >= 30, "R7")
m.addConstr(x_A <= 60, "R8")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")