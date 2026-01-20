import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
sets_I = ['color', 'bw']
parameters_P = {'color': 200, 'bw': 70}
M = 35

# 2. Model Initialization
m = gp.Model('color_bw_model')

# 3. Variables
x = {i: m.addVar(vtype=gp.GRB.CONTINUOUS, name=f'x_{i}') for i in sets_I}

# 4. Objective
m.setObjective(200 * x['color'] + 70 * x['bw'], GRB.MAXIMIZE)

# 5. Constraints
m.addConstr(x['color'] <= 20, 'constraint1')
m.addConstr(x['bw'] <= 30, 'constraint2')
m.addConstr(x['color'] + x['bw'] <= M, 'constraint3')

# 6. Optimization and Output
m.optimize()

if m.status == GRB.OPTIMAL:
    print('Optimal solution found:')
    for v in x.values():
        print(f'{v.varName} = {v.x}')
else:
    print('No optimal solution found.')

