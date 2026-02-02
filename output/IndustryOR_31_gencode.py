import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 124
price_A2 = 170
price_B1 = 124
price_B2 = 170
price_B3 = 170
cost_c_a1 = 170
cost_c_a2 = 170
cost_c_b1 = 170
cost_c_b2 = 170
cost_c_b3 = 170
limit_R1 = 1200
limit_R2 = 1510
limit_R3 = 800
limit_R4 = 1509

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x_i = m.addVar(vtype=GRB.INTEGER, name="x_i")
x_ii = m.addVar(vtype=GRB.INTEGER, name="x_ii")
x_iii = m.addVar(vtype=GRB.INTEGER, name="x_iii")

# 4. Objective (LaTeX structure + query numbers)
objective = gp.LinExpr()
objective += price_A1 * x_i
objective += price_A2 * x_ii
objective += price_B1 * x_iii
objective -= cost_c_a1 * limit_R1 * x_i
objective -= cost_c_a2 * limit_R1 * x_i
objective -= cost_c_b1 * limit_R3 * x_ii
objective -= cost_c_b2 * limit_R3 * x_ii
objective -= cost_c_b3 * limit_R3 * x_iii
m.setObjective(objective, GRB.MAXIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x_i <= limit_R1, "R1")
m.addConstr(x_i + x_iii <= limit_R2, "R2")
m.addConstr(x_ii <= limit_R3, "R3")
m.addConstr(x_i + x_ii + x_iii <= limit_R4, "R4")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")