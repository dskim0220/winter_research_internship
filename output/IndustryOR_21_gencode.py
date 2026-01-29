import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_A = 120
price_B = 110
price_C = 100
demand_A = 5300
demand_B = 3
demand_C = 3
max_tables = 600
min_tables = 150
at_least_three_orders_from_B = 3
supplier_AB_dependent = 3
supplier_BC_dependent = 1
sum_of_orders_from_A_and_B = 25
sum_of_orders_from_B_and_C = 30
at_least_seven_orders = 7

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x_A = m.addVar(vtype=GRB.INTEGER, name="orders_A")
x_B = m.addVar(vtype=GRB.INTEGER, name="orders_B")
x_C = m.addVar(vtype=GRB.INTEGER, name="orders_C")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(price_A * x_A + price_B * x_B + price_C * x_C, GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(20 * x_A + 15 * x_B + 15 * x_C >= min_tables, "TotalTables")
m.addConstr(20 * x_A + 15 * x_B + 15 * x_C <= max_tables, "MaxTables")
m.addConstr(x_B >= at_least_three_orders_from_B, "AtLeastThreeOrdersFromB")
m.addConstr(x_B >= supplier_AB_dependent * x_A, "SupplierABDependent")
m.addConstr(x_B >= supplier_BC_dependent * x_C, "SupplierBCDependent")
m.addConstr(x_A + x_B >= sum_of_orders_from_A_and_B, "SumOfOrdersFromAAndB")
m.addConstr(x_B + x_C >= sum_of_orders_from_B_and_C, "SumOfOrdersFromBAndC")
m.addConstr(x_A + x_B + x_C >= at_least_seven_orders, "AtLeastSevenOrders")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName}: {v.x}')
print(f'Total Objective Value: {m.objVal}')