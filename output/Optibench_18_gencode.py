import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 170000
cost_A1 = 170000
limit_A1 = 1
price_T1 = 124
cost_T1 = 124
limit_T1 = 1
price_L1 = 100
cost_L1 = 100
limit_L1 = 1

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x1 = m.addVar(vtype=GRB.INTEGER, name="x1")
x2 = m.addVar(vtype=GRB.INTEGER, name="x2")
x3 = m.addVar(vtype=GRB.INTEGER, name="x3")
x4 = m.addVar(vtype=GRB.INTEGER, name="x4")
y1 = m.addVar(vtype=GRB.BINARY, name="y1")
y2 = m.addVar(vtype=GRB.BINARY, name="y2")
y3 = m.addVar(vtype=GRB.BINARY, name="y3")
y4 = m.addVar(vtype=GRB.BINARY, name="y4")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(x1 + x2 + x3 + x4, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x1 + x2 + x3 + x4 >= 1, "R1")
m.addConstr(x1 + x2 + x3 + x4 <= 4, "R2")
m.addConstr(x1 + x2 + x3 + x4 <= 50, "R3")
m.addConstr(x1 + x2 + x3 + x4 <= 20 * y1 + 20 * y2 + 20 * y3 + 20 * y4, "R4")
m.addConstr(x1 + x2 + x3 + x4 <= 30 - 20 * y3, "R5")
m.addConstr(x1 + x2 + x3 + x4 <= 10 * y3, "R6")
m.addConstr(x1 * cost_A1 + x2 * cost_T1 + x3 * cost_L1 + x4 * cost_A1 >= 1000, "R7")
m.addConstr(x1 * price_A1 + x2 * price_T1 + x3 * price_L1 + x4 * price_A1 >= 800, "R8")
m.addConstr(x1 * cost_A1 + x2 * cost_T1 + x3 * cost_L1 + x4 * cost_A1 >= 600, "R9")
m.addConstr(y1 + y2 + y3 + y4 <= limit_A1, "R10")
m.addConstr(y1 + y2 + y3 + y4 >= limit_T1, "R11")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")