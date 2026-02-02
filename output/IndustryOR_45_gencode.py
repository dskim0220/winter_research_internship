import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 170000
price_A2 = 124

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x1 = m.addVar(vtype=GRB.INTEGER, name="x1")
x2 = m.addVar(vtype=GRB.INTEGER, name="x2")
x3 = m.addVar(vtype=GRB.INTEGER, name="x3")
x4 = m.addVar(vtype=GRB.INTEGER, name="x4")
x5 = m.addVar(vtype=GRB.INTEGER, name="x5")
x6 = m.addVar(vtype=GRB.INTEGER, name="x6")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(10.0*x1 + 10.0*x2 + 9.9*x3 + 9.8*x4 + 10.8*x5 + 11.3*x6, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 == 1, "R1")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 >= 8, "R2")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 >= 7, "R3")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 <= 2, "R4")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 <= 3, "R5")
m.addConstr(x5 + x6 <= 14, "R6")
m.addConstr(x5 <= 2, "R7")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 >= 70, "R8")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")