import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_A1 = 170000  # Assuming this is the cost of the direct A -> E link in some units

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
x_AB = m.addVar(name="x_AB")
x_AC = m.addVar(name="x_AC")
x_AD = m.addVar(name="x_AD")
x_AE = m.addVar(name="x_AE", lb=0)
x_BE = m.addVar(name="x_BE", lb=0)
x_CD = m.addVar(name="x_CD", lb=0)
x_DE = m.addVar(name="x_DE", lb=0)

# 4. Objective (LaTeX structure + query numbers)
m.setObjective(x_AE, GRB.MAXIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(x_AC + x_CD + x_DE >= x_AE, "Rule 5")
m.addConstr(x_AD + x_DE >= x_AE, "Rule 2")
m.addConstr(x_AC + x_CE <= x_AE, "Rule 3")
m.addConstr(x_AD + x_DE <= x_AE, "Rule 4")
m.addConstr(x_AB + x_BE <= x_AE, "Rule 7")
m.addConstr(x_AB + x_BD + x_DE <= x_AE, "Rule 8")
m.addConstr(x_AB + x_BC + x_CE <= x_AE, "Rule 9")
m.addConstr(x_AB + x_BD + x_DC + x_CE <= x_AE, "Rule 10")
m.addConstr(x_AB + x_BC + x_CD + x_DE <= x_AE, "Rule 11")
m.addConstr(x_AB + x_BC + x_CD + x_DE + x_EA <= x_AE, "Rule 12")
m.addConstr(x_AB + x_BC + x_CD + x_DE + x_EB <= x_AE, "Rule 13")
m.addConstr(x_AB + x_BC + x_CD + x_DE + x_EC <= x_AE, "Rule 14")
m.addConstr(x_AB + x_BC + x_CD + x_DE + x_ED <= x_AE, "Rule 15")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")