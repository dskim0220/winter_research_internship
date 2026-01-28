import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_A1 = 10
price_A2 = 5
price_A3 = 3
demand_A1 = 1000
demand_A2 = 800
demand_A3 = 600
workers_per_line = [20, 20, 20, 20]
max_workers_other_lines = 30
max_workers_3 = 10
full_line_min_workers = 20

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
hours = m.addVars(4, 3, name="hours", vtype=GRB.CONTINUOUS, obj=price_A1*10 + price_A2*5 + price_A3*3)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(hours.prod(price_A1, price_A2, price_A3), GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(hours.sum(0, 3).sum(1, 2) >= demand_A1, "Demand_Satisfaction")
m.addConstr(hours.sum(0, 3).sum(1, 2) >= demand_A2, "Demand_Satisfaction")
m.addConstr(hours.sum(0, 3).sum(1, 2) >= demand_A3, "Demand_Satisfaction")
m.addConstr(hours.sum(0, 3).sum(1, 2) <= 50, "Worker_Limitation")
m.addConstr(hours.sum(0, 3).sum(1, 2) <= workers_per_line[0]*100 + workers_per_line[1]*100 + workers_per_line[2]*100 + workers_per_line[3]*100, "Line_Limitation")
m.addConstr(hours.sum(0, 2).sum(1, 3) <= max_workers_other_lines*100, "Other_Lines_Limitation")
m.addConstr(hours.sum(0, 2).sum(1, 3) + hours.sum(1, 2).sum(0, 3) + hours.sum(2, 2).sum(0, 3) <= 2*100, "No_Three_Full")
m.addConstr(hours[2] <= max_workers_3*100, "Line_3_Limitation")
m.addConstr(hours[2] <= full_line_min_workers*100, "Full_Line_Min_Workers")

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)