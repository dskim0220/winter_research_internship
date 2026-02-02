import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 170000
cost_A1 = 124
limit_budget = 2500000

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x_AppX = m.addVar(vtype=GRB.INTEGER, name="x_AppX")
x_AppY = m.addVar(vtype=GRB.INTEGER, name="x_AppY")
x_AppZ = m.addVar(vtype=GRB.INTEGER, name="x_AppZ")
x_AppW = m.addVar(vtype=GRB.INTEGER, name="x_AppW")
x_AppV = m.addVar(vtype=GRB.INTEGER, name="x_AppV")

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(
    170000 * x_AppX - 124 * x_AppX - 0 * x_AppX +
    170000 * x_AppY - 124 * x_AppY - 0 * x_AppY +
    170000 * x_AppZ - 124 * x_AppZ - 0 * x_AppZ +
    170000 * x_AppW - 124 * x_AppW - 0 * x_AppW +
    170000 * x_AppV - 124 * x_AppV - 0 * x_AppV,
    GRB.MAXIMIZE
)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x_AppX + x_AppY + x_AppW + x_AppV <= 10, "R1")
m.addConstr(x_AppZ + x_AppV <= 28, "R2")
m.addConstr(x_AppX >= 2 * x_AppY, "R3")
m.addConstr(x_AppX + x_AppY + x_AppW + x_AppV >= 2, "R4")
m.addConstr(x_AppX + x_AppY + x_AppZ + x_AppW + x_AppV <= 30, "R5")
m.addConstr(x_AppX + x_AppY + x_AppZ + x_AppW + x_AppV >= 1, "R6")
m.addConstr(price_A1 * x_AppX + price_A1 * x_AppY + price_A1 * x_AppZ + price_A1 * x_AppW + price_A1 * x_AppV <= limit_budget, "R7")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")