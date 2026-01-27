import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
prices = {'A1': 53 * 124, 'A2': 45 * 109, 'A3': 54 * 115}
production_costs = {'A1': 0, 'A2': 0, 'A3': 0}
activation_costs = {'A1': 0, 'A2': 0, 'A3': 0}
fixed_costs = {'A1': 0, 'A2': 0, 'A3': 0}
minimum_batches = {'A1': 0, 'A2': 0, 'A3': 0}
demand = {'A1': 0, 'A2': 0, 'A3': 0}
total_production_limit = 0
activation_time = {'A1': 0 / 60, 'A2': 0 / 60, 'A3': 0 / 60}
days = 0

# 2. Model Initialization
m = gp.Model("production_model")

# 3. Variables
x_A1 = m.addVar(vtype=gp.GRB.BINARY, name="x_A1")
x_A2 = m.addVar(vtype=gp.GRB.BINARY, name="x_A2")
x_A3 = m.addVar(vtype=gp.GRB.BINARY, name="x_A3")

# 4. Objective
obj = prices['A1'] * x_A1 + prices['A2'] * x_A2 + prices['A3'] * x_A3 - activation_costs['A1'] * x_A1 - activation_costs['A2'] * x_A2 - activation_costs['A3'] * x_A3 - fixed_costs['A1'] * x_A1 - fixed_costs['A2'] * x_A2 - fixed_costs['A3'] * x_A3
m.setObjective(obj, GRB.MAXIMIZE)

# 5. Constraints
m.addConstr(x_A1 <= total_production_limit, "Cap_A1")
m.addConstr(x_A2 <= total_production_limit, "Cap_A2")
m.addConstr(x_A3 <= total_production_limit, "Cap_A3")
m.addConstr(x_A1 + activation_time['A1'] >= 1, "Min_A1")
m.addConstr(x_A1 + x_A2 + x_A3 <= days, "Sum_A1_A2_A3")
m.addConstr(prices['A1'] * x_A1 + prices['A2'] * x_A2 + prices['A3'] * x_A3 <= total_production_limit, "Prod_A1_A2_A3")

# 6. Optimization and Output
m.optimize()

if m.status == GRB.OPTIMAL:
    print('Optimal Solution:')
    print(f"x_A1 = {x_A1.x}")
    print(f"x_A2 = {x_A2.x}")
    print(f"x_A3 = {x_A3.x}")
else:
    print('No optimal solution found.')