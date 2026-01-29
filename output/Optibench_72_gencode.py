import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_APPX = 100000
price_APPY = 150000
price_APPZ = 200000
price_APPW = 120000
price_APPV = 180000
cost_APPX = 60000
cost_APPY = 70000
cost_APPZ = 80000
cost_APPW = 90000
cost_APPV = 110000
demand_APPX = 1210
demand_APPY = 1090
demand_APPZ = 1700
demand_APPW = 1500
demand_APPV = 1300

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
y_APPX = m.addVar(vtype=GRB.BINARY, name="y_APPX")
y_APPY = m.addVar(vtype=GRB.BINARY, name="y_APPY")
y_APPZ = m.addVar(vtype=GRB.BINARY, name="y_APPZ")
y_APPW = m.addVar(vtype=GRB.BINARY, name="y_APPW")
y_APPV = m.addVar(vtype=GRB.BINARY, name="y_APPV")
x_APPX = m.addVar(vtype=GRB.INTEGER, name="x_APPX")
x_APPY = m.addVar(vtype=GRB.INTEGER, name="x_APPY")
x_APPZ = m.addVar(vtype=GRB.INTEGER, name="x_APPZ")
x_APPW = m.addVar(vtype=GRB.INTEGER, name="x_APPW")
x_APPV = m.addVar(vtype=GRB.INTEGER, name="x_APPV")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(price_APPX * x_APPX + price_APPY * x_APPY + price_APPZ * x_APPZ + price_APPW * x_APPW + price_APPV * x_APPV, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x_APPX == y_APPX * demand_APPX, "Constraint1")
m.addConstr(x_APPY == y_APPY * demand_APPY, "Constraint2")
m.addConstr(x_APPZ == y_APPZ * demand_APPZ, "Constraint3")
m.addConstr(x_APPW == y_APPW * demand_APPW, "Constraint4")
m.addConstr(x_APPV == y_APPV * demand_APPV, "Constraint5")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Optimal Objective Value = {m.objVal}')