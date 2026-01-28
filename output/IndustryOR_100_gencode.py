import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
bandwidth_AB = 90
bandwidth_AC = 85
bandwidth_AD = 67
bandwidth_BC = 70
bandwidth_CD = 25
bandwidth_CE = 80
bandwidth_DE = 56
transmission_efficiency_AE_direct = 10
transmission_efficiency_AE_indirect = 96
min_bandwidth_AE_direct = 65
min_bandwidth_AE_indirect = 80
min_bandwidth_sum = 100

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
link_AE_direct = m.addVar(name="link_AE_direct", obj=1, lb=min_bandwidth_AE_direct, ub=min_bandwidth_AE_indirect, vtype=GRB.CONTINUOUS)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(link_AE_direct, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(bandwidth_AC + bandwidth_CE + link_AE_direct >= min_bandwidth_sum, name="sum_bandwidth_constraint")
m.addConstr(bandwidth_CE + link_AE_direct <= min_bandwidth_AE_indirect, name="indirect_bandwidth_constraint")
m.addConstr(bandwidth_AC + link_AE_direct >= min_bandwidth_AE_direct, name="direct_bandwidth_constraint")
m.addConstr((1 - (transmission_efficiency_AE_direct / 100)) * link_AE_direct == min_bandwidth_AE_direct, name="efficiency_constraint_AE_direct")
m.addConstr((1 - (transmission_efficiency_AE_indirect / 100)) * link_AE_direct == min_bandwidth_AE_indirect, name="efficiency_constraint_AE_indirect")

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)