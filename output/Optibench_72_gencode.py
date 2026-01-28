import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_APPX = 100000
price_APPY = 150000
price_APPZ = 200000
price_APPW = 120000
price_APPV = 180000
cost_APPX = 60000
cost_APPY = 80000
cost_APPZ = 100000
cost_APPW = 70000
cost_APPV = 90000
marketing_cost_APPX = 20000
marketing_cost_APPY = 30000
marketing_cost_APPZ = 40000
marketing_cost_APPW = 25000
marketing_cost_APPV = 35000
min_ratio_APPX_APPY = 2
total_teams_available = 30
marketing_budget = 2500000
min_APPX_teams = 2
max_APPX_APPY_APPW_APPV_teams = 10
max_APPZ_APPV_teams = 28

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
teams_APPX = m.addVar(vtype=GRB.CONTINUOUS, name="teams_APPX")
teams_APPY = m.addVar(vtype=GRB.CONTINUOUS, name="teams_APPY")
teams_APPZ = m.addVar(vtype=GRB.CONTINUOUS, name="teams_APPZ")
teams_APPW = m.addVar(vtype=GRB.CONTINUOUS, name="teams_APPW")
teams_APPV = m.addVar(vtype=GRB.CONTINUOUS, name="teams_APPV")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    price_APPX * teams_APPX +
    price_APPY * teams_APPY +
    price_APPZ * teams_APPZ +
    price_APPW * teams_APPW +
    price_APPV * teams_APPV,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(teams_APPX + teams_APPY + teams_APPZ + teams_APPW + teams_APPV <= total_teams_available, "total_teams_constraint")
m.addConstr(teams_APPX / teams_APPY >= min_ratio_APPX_APPY, "ratio_constraint")
m.addConstr(teams_APPX + teams_APPY + teams_APPW + teams_APPV <= max_APPX_APPY_APPW_APPV_teams, "max_APPX_APPY_APPW_APPV_teams_constraint")
m.addConstr(teams_APPZ + teams_APPV <= max_APPZ_APPV_teams, "max_APPZ_APPV_teams_constraint")
m.addConstr(teams_APPX + teams_APPY + teams_APPZ + teams_APPW + teams_APPV >= min_APPX_teams, "min_APPX_teams_constraint")
m.addConstr(teams_APPX * marketing_cost_APPX + teams_APPY * marketing_cost_APPY + teams_APPZ * marketing_cost_APPZ + teams_APPW * marketing_cost_APPW + teams_APPV * marketing_cost_APPV <= marketing_budget, "marketing_budget_constraint")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Maximum Revenue: {m.objVal}')