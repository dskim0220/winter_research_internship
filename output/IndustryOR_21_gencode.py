import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
sets_A = ['A', 'B', 'C']
parameters_c = {'A': 120, 'B': 110, 'C': 100}
parameters_t = {'A': 20, 'B': 15, 'C': 15}
parameters_m = 150
parameters_M = 600
parameters_o = {'A -> B': 30}

# 2. Model Initialization
m = gp.Model("operation_research_model")

# 3. Variables
x_A = m.addVar(vtype=gp.GRB.CONTINUOUS, name="xA")
x_B = m.addVar(vtype=gp.GRB.CONTINUOUS, name="xB")
x_C = m.addVar(vtype=gp.GRB.CONTINUOUS, name="xC")

# 4. Objective
m.setObjective(gp.quicksum(parameters_c[var] * x for var in sets_A), GRB.MINIMIZE)

# 5. Constraints
m.addConstr(x_A + parameters_t['B'] * x_B + parameters_t['C'] * x_C >= parameters_m, "Constraint1")
m.addConstr(x_A + parameters_t['B'] * x_B + parameters_t['C'] * x_C <= parameters_M, "Constraint2")
m.addConstr(parameters_o['A -> B'] <= x_B, "Constraint3")
m.addConstr(x_B > 0, "AuxiliaryConstraint")
m.addConstr(x_C >= parameters_o['A -> B'], "AuxiliaryConstraint2")

# 6. Optimization and Output
m.optimize()

print(f'Optimal objective value: {m.objVal}')
for v in m.getVars():
    print(f'{v.varName} = {v.x}')

if m.status == GRB.OPTIMAL:
    print("The model is optimal.")
else:
    print("The model is not optimal.")