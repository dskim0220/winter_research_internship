import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_NY = 20
price_LA = 40
price_CH = 30
price_ATL = 15
fixed_cost_NY = 400
fixed_cost_LA = 500
fixed_cost_CH = 300
fixed_cost_ATL = 150
demand_Region_1 = 80
demand_Region_2 = 70
demand_Region_3 = 40
total_demand = demand_Region_1 + demand_Region_2 + demand_Region_3

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
y_NY = m.addVar(vtype=GRB.BINARY, name="y_NY")
y_LA = m.addVar(vtype=GRB.BINARY, name="y_LA")
y_CH = m.addVar(vtype=GRB.BINARY, name="y_CH")
y_ATL = m.addVar(vtype=GRB.BINARY, name="y_ATL")
x_NY = m.addVar(vtype=GRB.INTEGER, name="x_NY")
x_LA = m.addVar(vtype=GRB.INTEGER, name="x_LA")
x_CH = m.addVar(vtype=GRB.INTEGER, name="x_CH")
x_ATL = m.addVar(vtype=GRB.INTEGER, name="x_ATL")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(x_NY * price_NY + x_LA * price_LA + x_CH * price_CH + x_ATL * price_ATL, GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x_NY <= 100 * y_NY, "Constraint_NY")
m.addConstr(x_LA <= 100 * y_LA, "Constraint_LA")
m.addConstr(x_CH <= 100 * y_CH, "Constraint_CH")
m.addConstr(x_ATL <= 100 * y_ATL, "Constraint_ATL")

m.addConstr(x_NY + x_LA + x_CH + x_ATL >= demand_Region_1, "Constraint_Region_1")
m.addConstr(x_NY + x_LA + x_CH + x_ATL >= demand_Region_2, "Constraint_Region_2")
m.addConstr(x_NY + x_LA + x_CH + x_ATL >= demand_Region_3, "Constraint_Region_3")

# 6. Optimization and Output
m.optimize()

# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')

print(f'Total Cost: {m.objVal}')