import gurobipy as gp
from gurobipy import GRB

# Constants (Derived from 'query' values)
c_A = 120
c_B = 110
c_C = 100
u_A = 20
u_B = 15
u_C = 15
M = 10000

# Model Initialization
m = gp.Model("optimization_model")

# Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x_A = m.addVar(vtype=GRB.INTEGER, name="x_A")
x_B = m.addVar(vtype=GRB.INTEGER, name="x_B")
x_C = m.addVar(vtype=GRB.INTEGER, name="x_C")
y_A = m.addVar(vtype=GRB.BINARY, name="y_A")
y_B = m.addVar(vtype=GRB.BINARY, name="y_B")

# Objective (LaTeX structure + query numbers)
m.setObjective(c_A * x_A * u_A + c_B * x_B * u_B + c_C * x_C * u_C, GRB.MINIMIZE)

# Constraints (LaTeX structure + query numbers)
m.addConstr(x_A * u_A + x_B * u_B + x_C * u_C >= 150, name="C1")
m.addConstr(x_A * u_A + x_B * u_B + x_C * u_C <= 600, name="C2")
m.addConstr(x_B * u_B >= 30 * y_A, name="C3")
m.addConstr(x_C >= y_B, name="C4")
m.addConstr(x_A * u_A + x_B * u_B >= 25 * y_A, name="C5")
m.addConstr(x_B * u_B + x_C * u_C >= 30 * y_B, name="C6")
m.addConstr(x_A + x_B + x_C >= 7, name="C7")
m.addConstr(x_A * u_A <= 60, name="C8")
m.addConstr(y_A <= M * (1 - gp.quicksum([x_A == 0])), name="C9")
m.addConstr(y_B <= M * (1 - gp.quicksum([x_B == 0])), name="C10")

# Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    print(f"Optimal Objective Value: {m.objVal}")
    for v in m.getVars():
        if v.x > 1e-6:
            print(f"{v.varName}: {v.x}")
else:
    print("Optimization was not successful.")