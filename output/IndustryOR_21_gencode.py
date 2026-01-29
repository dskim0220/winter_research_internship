import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_A = 120
price_B = 110
price_C = 100
cost_A = 20
cost_B = 15
cost_C = 15
min_order_A = 150
min_orders_total = 7
max_order_A = 60
min_order_B_given_A = 30
min_order_C_given_B = 1
min_sum_AB = 25
min_sum_BC = 30
max_total_tables = 600

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x_A1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="x_A1")
x_B1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="x_B1")
x_C1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="x_C1")

y_A1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="y_A1")
y_B1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="y_B1")
y_C1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="y_C1")

z_A1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="z_A1")
z_B1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="z_B1")
z_C1 = m.addVars(range(1, 8), vtype=GRB.BINARY, name="z_C1")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_A * x_A1.prod(cost_A) +
    price_B * x_B1.prod(cost_B) +
    price_C * x_C1.prod(cost_C),
    GRB.MINIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x_A1.sum() >= min_order_A)
m.addConstr(x_B1.sum() >= min_order_B_given_A)
m.addConstr(x_C1.sum() >= min_order_C_given_B)
m.addConstr(x_A1.sum() + x_B1.sum() >= min_sum_AB)
m.addConstr(x_B1.sum() + x_C1.sum() >= min_sum_BC)
m.addConstr(x_A1.sum() + x_B1.sum() + x_C1.sum() <= max_total_tables)

# 6. Optimization and Output
m.optimize()

# Print results for each variable
for var in m.getVars():
    print(f'{var.varName}: {var.x}')