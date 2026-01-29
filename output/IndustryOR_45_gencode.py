import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_1 = 10.0
price_2 = 10.0
price_3 = 9.9
price_4 = 9.8
price_5 = 10.8
price_6 = 11.3
monday_1 = 6
tuesday_1 = 5
wednesday_1 = 7
thursday_1 = 4
friday_1 = 5
monday_2 = 5
tuesday_2 = 4
wednesday_2 = 6
thursday_2 = 3
friday_2 = 4
monday_3 = 5
tuesday_3 = 4
wednesday_3 = 6
thursday_3 = 3
friday_3 = 4
monday_4 = 5
tuesday_4 = 4
wednesday_4 = 6
thursday_4 = 3
friday_4 = 4
monday_5 = 5
tuesday_5 = 4
wednesday_5 = 6
thursday_5 = 3
friday_5 = 4
monday_6 = 5
tuesday_6 = 4
wednesday_6 = 6
thursday_6 = 3
friday_6 = 4

# 2. Model Initialization
m = gp.Model("student_work_schedule")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.INTEGER, name="x1")
x2 = m.addVar(vtype=GRB.INTEGER, name="x2")
x3 = m.addVar(vtype=GRB.INTEGER, name="x3")
x4 = m.addVar(vtype=GRB.INTEGER, name="x4")
x5 = m.addVar(vtype=GRB.INTEGER, name="x5")
x6 = m.addVar(vtype=GRB.INTEGER, name="x6")

y1 = m.addVar(vtype=GRB.BINARY, name="y1")
y2 = m.addVar(vtype=GRB.BINARY, name="y2")
y3 = m.addVar(vtype=GRB.BINARY, name="y3")
y4 = m.addVar(vtype=GRB.BINARY, name="y4")
y5 = m.addVar(vtype=GRB.BINARY, name="y5")
y6 = m.addVar(vtype=GRB.BINARY, name="y6")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(price_1 * x1 + price_2 * x2 + price_3 * x3 + price_4 * x4 + price_5 * x5 + price_6 * x6, GRB.MAXIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 <= monday_1 * y1, "Monday Constraint 1")
m.addConstr(x2 <= tuesday_1 * y2, "Tuesday Constraint 1")
m.addConstr(x3 <= wednesday_1 * y3, "Wednesday Constraint 1")
m.addConstr(x4 <= thursday_1 * y4, "Thursday Constraint 1")
m.addConstr(x5 <= friday_1 * y5, "Friday Constraint 1")
m.addConstr(x6 <= monday_2 * y6, "Monday Constraint 2")
m.addConstr(x1 <= tuesday_2 * y1, "Tuesday Constraint 2")
m.addConstr(x2 <= wednesday_2 * y2, "Wednesday Constraint 2")
m.addConstr(x3 <= thursday_2 * y3, "Thursday Constraint 2")
m.addConstr(x4 <= friday_2 * y4, "Friday Constraint 2")
m.addConstr(x5 <= monday_3 * y5, "Monday Constraint 3")
m.addConstr(x6 <= tuesday_3 * y6, "Tuesday Constraint 3")
m.addConstr(x1 <= wednesday_3 * y1, "Wednesday Constraint 3")
m.addConstr(x2 <= thursday_3 * y2, "Thursday Constraint 3")
m.addConstr(x3 <= friday_3 * y3, "Friday Constraint 3")
m.addConstr(x4 <= monday_4 * y4, "Monday Constraint 4")
m.addConstr(x5 <= tuesday_4 * y5, "Tuesday