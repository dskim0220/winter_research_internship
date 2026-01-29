import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
employees_monday = 15
employees_tuesday = 13
employees_wednesday = 15
price_monday = 15
price_tuesday = 13
price_wednesday = 15
M = 1000000

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
y_monday = m.addVar(vtype=GRB.BINARY, name="y_monday")
y_tuesday = m.addVar(vtype=GRB.BINARY, name="y_tuesday")
y_wednesday = m.addVar(vtype=GRB.BINARY, name="y_wednesday")
x_monday = m.addVar(vtype=GRB.INTEGER, name="x_monday")
x_tuesday = m.addVar(vtype=GRB.INTEGER, name="x_tuesday")
x_wednesday = m.addVar(vtype=GRB.INTEGER, name="x_wednesday")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(price_monday * x_monday + price_tuesday * x_tuesday + price_wednesday * x_wednesday, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x_monday <= employees_monday * y_monday, "Constraint_Monday_Employees")
m.addConstr(x_tuesday <= employees_tuesday * y_tuesday, "Constraint_Tuesday_Employees")
m.addConstr(x_wednesday <= employees_wednesday * y_wednesday, "Constraint_Wednesday_Employees")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print('Optimal Objective Value:', m.objVal)