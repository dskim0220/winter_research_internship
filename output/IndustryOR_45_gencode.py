import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
price_A1 = 124
price_A2 = 109
price_A3 = 105
price_A4 = 110
price_A5 = 115
price_A6 = 120
min_hours_undergraduates = 8
min_hours_graduate_students = 7
max_hours_per_student = 2
max_students_per_day = 3
total_duty_hours = 70
max_hours_5_and_6 = 14
thursday_limit_5 = 2

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
hours_student_1 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_1")
hours_student_2 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_2")
hours_student_3 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_3")
hours_student_4 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_4")
hours_student_5 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_5")
hours_student_6 = m.addVar(vtype=GRB.CONTINUOUS, name="hours_student_6")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    hours_student_1 * price_A1 + 
    hours_student_2 * price_A2 + 
    hours_student_3 * price_A3 + 
    hours_student_4 * price_A4 + 
    hours_student_5 * price_A5 + 
    hours_student_6 * price_A6, 
    GRB.MINIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(hours_student_1 + hours_student_2 + hours_student_3 + hours_student_4 >= min_hours_undergraduates, "Total_hours_undergraduates")
m.addConstr(hours_student_5 + hours_student_6 >= min_hours_graduate_students, "Total_hours_graduate_students")
m.addConstr(hours_student_1 + hours_student_2 + hours_student_3 + hours_student_4 + hours_student_5 + hours_student_6 <= total_duty_hours, "SUM(hours_student_1, hours_student_2, hours_student_3, hours_student_4, hours_student_5, hours_student_6)")
m.addConstr(hours_student_5 + hours_student_6 <= max_hours_5_and_6, "SUM(hours_student_5, hours_student_6) <= MAX_HOURS_5_AND_6")
m.addConstr(hours_student_5 <= thursday_limit_5, "hours_student_5 <= THURSDAY_LIMIT_5")

# 6. Optimization and Output
m.optimize()
# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Total Objective Value = {m.objVal}')