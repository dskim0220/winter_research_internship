import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
x = 10  # Number of trucks allocated for GoodsX
y = 15  # Number of trucks allocated for GoodsY
z = 25  # Number of trucks allocated for GoodsZ
b = 1  # Optimization software investment decision (1 if invested)
price_A1 = 1000  # Cost reduction per $100 invested in optimization
cost_reduction_A1 = 10  # Cost reduction for GoodsX
cost_reduction_A2 = 12  # Cost reduction for GoodsY
cost_reduction_A3 = 15  # Cost reduction for GoodsZ
total_trucks_limit = 50  # Total trucks constraint
goodsX_trucks_min = 10  # GoodsX trucks constraint
goodsY_trucks_min = 15  # GoodsY trucks constraint
goodsZ_trucks_max = 25  # GoodsZ trucks constraint
goodsZ_cost_reduction_max = 3750  # Cost reduction constraint for GoodsZ
total_cost_reduction_min = 0  # Total cost reduction constraint
investment_limit = 10000  # Investment constraint

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x_var = m.addVar(vtype=GRB.INTEGER, name="x")
y_var = m.addVar(vtype=GRB.INTEGER, name="y")
z_var = m.addVar(vtype=GRB.INTEGER, name="z")
b_var = m.addVar(vtype=GRB.BINARY, name="b")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(x_var * cost_reduction_A1 + y_var * cost_reduction_A2 + z_var * cost_reduction_A3 - b_var * price_A1 * x_var - b_var * price_A2 * y_var - b_var * price_A3 * z_var, GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x_var + y_var + z_var <= total_trucks_limit, "TotalTrucksConstraint")
m.addConstr(x_var >= goodsX_trucks_min, "GoodsXTrucksConstraint")
m.addConstr(y_var >= goodsY_trucks_min, "GoodsYTrucksConstraint")
m.addConstr(z_var <= goodsZ_trucks_max, "GoodsZTrucksConstraint")
m.addConstr(x_var * cost_reduction_A1 + y_var * cost_reduction_A2 + z_var * cost_reduction_A3 <= goodsZ_cost_reduction_max, "GoodsZCostReductionConstraint")
m.addConstr(x_var * cost_reduction_A1 + y_var * cost_reduction_A2 + z_var * cost_reduction_A3 >= total_cost_reduction_min, "TotalCostReductionConstraint")
m.addConstr(b_var <= investment_limit, "InvestmentConstraint")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Total Objective Value = {m.objVal}')