import gurobipy as gp
from gurobipy import GRB
import json
import argparse

# 1. Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, required=True, help='Path to instance_data.json')
args = parser.parse_args()

# 2. Data Loading
with open(args.data, 'r', encoding='utf-8') as f:
    inst_data = json.load(f)

params = inst_data.get('parameters', {})
sets = inst_data.get('sets', {})

# 3. Model Initialization
m = gp.Model("optimization_model")

# 4. Sets & Variables
x_A = m.addVar(vtype=GRB.INTEGER, name="x_A")
x_B = m.addVar(vtype=GRB.INTEGER, name="x_B")
x_C = m.addVar(vtype=GRB.INTEGER, name="x_C")
y_A = m.addVar(vtype=GRB.BINARY, name="y_A")
y_B = m.addVar(vtype=GRB.BINARY, name="y_B")
y_C = m.addVar(vtype=GRB.BINARY, name="y_C")

# 5. Objective & Constraints
m.setObjective(params['cost_A'] * x_A + params['cost_B'] * x_B + params['cost_C'] * x_C, GRB.MINIMIZE)

m.addConstr(x_A >= y_A)
m.addConstr(x_B >= y_B)
m.addConstr(x_C >= y_C)

# Demand satisfaction constraints
m.addConstr(params['units_A'] * x_A + params['units_B'] * x_B + params['units_C'] * x_C >= params['min_total'])
m.addConstr(params['units_A'] * x_A + params['units_B'] * x_B + params['units_C'] * x_C <= params['max_total'])

# Indicator linking constraints
m.addConstr(params['units_B'] * x_B >= params['min_qty_B_if_A'] * y_A)
m.addConstr((params['units_A'] * x_A + params['units_B'] * x_B) >= params['min_sum_AB'] * y_A)
m.addConstr((params['units_B'] * x_B + params['units_C'] * x_C) >= params['min_sum_BC'] * y_B)

# Order frequency constraint
m.addConstr(x_A + x_B + x_C >= params['min_orders'])

# Additional constraints based on the provided formulation
m.addConstr(params['units_A'] * x_A <= params['max_units_A'])

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    print(f"Optimal Objective Value: {m.objVal}")
    for v in m.getVars():
        if v.x > 1e-6:
            print(f"{v.varName}: {v.x}")
else:
    print("Optimization was not successful.")