import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 170000
price_A2 = 170000
price_A3 = 170000
price_A4 = 170000
price_A5 = 170000
price_A6 = 170000
price_A7 = 170000

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x1 = m.addVar(vtype=GRB.INTEGER, name="x1")
x2 = m.addVar(vtype=GRB.INTEGER, name="x2")
x3 = m.addVar(vtype=GRB.INTEGER, name="x3")
x4 = m.addVar(vtype=GRB.INTEGER, name="x4")
x5 = m.addVar(vtype=GRB.INTEGER, name="x5")
x6 = m.addVar(vtype=GRB.INTEGER, name="x6")
x7 = m.addVar(vtype=GRB.INTEGER, name="x7")
y1 = m.addVar(vtype=GRB.BINARY, name="y1")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(x1 + x2 + x3 + x4 + x5 + x6 + x7, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x1 - x5 <= 7 * y1, "C1")
m.addConstr(x7 + x1 >= 3 * y1, "C2")

# 6. Optimization & Output
m.optimize()
if m.status == GRUBOpy.GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")