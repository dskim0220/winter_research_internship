import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
sets_A = ['A', 'B', 'C']
parameters_c = {'A': 120, 'B': 110, 'C': 100}
parameters_m_tables = 150
parameters_M_tables = 600
parameters_m_orders_A = 7
parameters_M_tables_A = 60
parameters_m_tables_AB = 25
parameters_m_tables_AC = 25
parameters_m_tables_BC = 30

# 2. Model Initialization
m = gp.Model("table_production")

# 3. Variables
variables_orders = {set_: m.addVar(vtype=GRB.CONTINUOUS, name=f"x_{set_}") for set_ in sets_A}

# 4. Objective
m.setObjective(gp.quicksum(parameters_c[set_] * variables_orders[set_] for set_ in sets_A), GRB.MINIMIZE)

# 5. Constraints
m.addConstr(gp.quicksum(parameters_c[set_] * 20 * variables_orders[set_] for set_ in sets_A) >= parameters_m_tables, "constraint1")
m.addConstr(gp.quicksum(parameters_c[set_] * 20 * variables_orders[set_] for set_ in sets_A) <= parameters_M_tables, "constraint2")
m.addConstr(variables_orders['A'] >= parameters_m_orders_A, "constraint3")
m.addConstr(variables_orders['A'] >= parameters_m_tables_AB - variables_orders['B'], "constraint4")
m.addConstr(variables_orders['B'] >= parameters_m_tables_AC - variables_orders['A'], "constraint5")
m.addConstr(variables_orders['C'] >= parameters_m_tables_BC - variables_orders['B'], "constraint6")
m.addConstr(variables_orders['A'] + variables_orders['B'] >= parameters_m_orders_A, "constraint7")
m.addConstr(variables_orders['A'] <= parameters_M_tables_A, "constraint8")

# 6. Optimization and Output
m.optimize()

print("Optimization finished.")
if m.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {m.objVal}")
    for var in variables_orders.values():
        print(f"{var.varName}: {var.x}")
else:
    print("The model is not optimal.")