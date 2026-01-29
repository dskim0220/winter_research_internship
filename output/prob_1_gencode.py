import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_color_printer = 200
profit_color_printer = 200
price_bw_printer = 70
profit_bw_printer = 70
color_printer_production_limit = 20
black_and_white_printer_production_limit = 30
paper_tray_installation_machine_limit = 35

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
num_color_printers = m.addVar(name="num_color_printers", obj=profit_color_printer, vtype=GRB.CONTINUOUS, lb=0, ub=color_printer_production_limit)
num_black_and_white_printers = m.addVar(name="num_black_and_white_printers", obj=profit_bw_printer, vtype=GRB.CONTINUOUS, lb=0, ub=black_and_white_printer_production_limit)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(num_color_printers * profit_color_printer + num_black_and_white_printers * profit_bw_printer, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(num_color_printers <= color_printer_production_limit, name="color_printer_production_limit")
m.addConstr(num_black_and_white_printers <= black_and_white_printer_production_limit, name="black_and_white_printer_production_limit")
m.addConstr(num_color_printers + num_black_and_white_printers <= paper_tray_installation_machine_limit, name="paper_tray_installation_machine_limit")

# 6. Optimization and Output
m.optimize()

# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Total Profit = {m.objVal}')