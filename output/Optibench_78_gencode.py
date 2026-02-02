import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
price_NY_to_LA = 170000
price_NY_to_CH = 180000
price_NY_to_AT = 190000
price_LA_to_LA = 160000
price_LA_to_CH = 170000
price_LA_to_AT = 180000
price_CH_to_LA = 150000
price_CH_to_CH = 140000
price_CH_to_AT = 160000
price_AT_to_LA = 140000
price_AT_to_CH = 150000
price_AT_to_AT = 130000
demand_NY = 100000
demand_LA = 120000
demand_CH = 110000
demand_AT = 90000

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
y_NY = m.addVar(vtype=GRB.BINARY, name="y_NY")
y_LA = m.addVar(vtype=GRB.BINARY, name="y_LA")
y_CH = m.addVar(vtype=GRB.BINARY, name="y_CH")
y_AT = m.addVar(vtype=GRB.BINARY, name="y_AT")

# 4. Objective (LaTeX structure + query numbers)
objective = gp.LinExpr()
objective += demand_NY * price_NY_to_LA * y_NY
objective += demand_NY * price_NY_to_CH * y_NY
objective += demand_NY * price_NY_to_AT * y_NY
objective += demand_LA * price_LA_to_LA * y_LA
objective += demand_LA * price_LA_to_CH * y_LA
objective += demand_LA * price_LA_to_AT * y_LA
objective += demand_CH * price_CH_to_LA * y_CH
objective += demand_CH * price_CH_to_CH * y_CH
objective += demand_CH * price_CH_to_AT * y_CH
objective += demand_AT * price_AT_to_LA * y_AT
objective += demand_AT * price_AT_to_CH * y_AT
objective += demand_AT * price_AT_to_AT * y_AT
m.setObjective(objective, GRB.MINIMIZE)

# 5. Constraints (LaTeX structure + query numbers)
m.addConstr(y_LA >= y_NY, "R1")
m.addConstr(y_NY + y_LA + y_CH + y_AT <= 2, "R2")
m.addConstr(y_AT + y_LA >= 1, "R3")
m.addConstr(y_NY + y_AT <= 1, "R4")
m.addConstr(y_NY + y_CH + y_LA >= 1, "R5")
m.addConstr(y_NY + y_CH >= 1, "R6")

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")