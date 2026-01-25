import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
sets = {
    'I': ['A1', 'A2', 'A3'],
    'J': range(1, 23)
}
parameters = {
    'A1': {'price': 100, 'demand': 1000, 'cost': 80, 'quota': 1000, 'activation_cost': 10,'min_batch': 10, 'total_production_limit': 1000,'min_prod_A1': 57},
    'A2': {'price': 150, 'demand': 1500, 'cost': 120, 'quota': 1500, 'activation_cost': 15,'min_batch': 15, 'total_production_limit': 1500,'min_prod_A2': 57},
    'A3': {'price': 200, 'demand': 2000, 'cost': 160, 'quota': 2000, 'activation_cost': 20,'min_batch': 20, 'total_production_limit': 2000,'min_prod_A3': 57}
}

# 2. Model Initialization
m = gp.Model('production_model')

# 3. Variables
x = {A: m.addVar(vtype=gp.GRB.BINARY, name=f'x_{A}') for A in sets['I']}

# 4. Objective
m.setObjective(gp.quicksum(parameters[A]['price'] * x[A] for A in sets['I']) - gp.quicksum(parameters[A]['cost'] * x[A] for A in sets['I']), gp.GRB.MAXIMIZE)

# 5. Constraints
m.addConstr(gp.quicksum(parameters[A]['demand'] * x[A] for A in sets['I']) <= parameters['total_production_limit'], 'DemandConstraint')
m.addConstr(gp.quicksum(parameters[A]['activation_cost'] * x[A] for A in sets['I']) <= parameters['total_production_limit'] * 100, 'ActivationCostConstraint')
m.addConstr(gp.quicksum(parameters[A]['min_batch'] * x[A] for A in sets['I']) <= parameters['total_production_limit'], 'MinBatchConstraint')
m.addConstr(gp.quicksum(parameters[A]['quota'] * x[A] for A in sets['I']) <= parameters['total_production_limit'], 'QuotaConstraint')
m.addConstr(gp.quicksum(parameters[A]['price'] * x[A] * parameters[A]['demand'] for A in sets['I']) <= parameters['total_production_limit'] * 100, 'RevenueConstraint')
m.addConstr(gp.quicksum(parameters[A]['cost'] * x[A] for A in sets['I']) <= parameters['total_production_limit'] * 100, 'FixedCostsConstraint')

# 6. Optimization and Output
m.optimize()

print('Optimization finished.')
if m.status == GRB.OPTIMAL:
    print(f'Optimal objective value: {m.objVal}')
    for v in m.getVars():
        print(f'{v.varName} = {v.x}')
else:
    print('The model is not optimal.')