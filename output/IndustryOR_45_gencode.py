import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
WAGE = {
    "Monday": 6,
    "Tuesday": 0,
    "Wednesday": 6,
    "Thursday": 0,
    "Friday": 7,
    "Monday": 0,
    "Tuesday": 8,
    "Wednesday": 9,
    "Thursday": 5,
    "Friday": 0,
    "Monday": 4,
    "Tuesday": 8,
    "Wednesday": 3,
    "Thursday": 0,
    "Friday": 5,
    "Monday": 5,
    "Tuesday": 5,
    "Wednesday": 6,
    "Thursday": 0,
    "Friday": 4,
    "Monday": 3,
    "Tuesday": 0,
    "Wednesday": 5,
    "Thursday": 8,
    "Friday": 0,
    "Monday": 0,
    "Tuesday": 6,
    "Wednesday": 0,
    "Thursday": 6,
    "Friday": 5
}
HOURS = {
    "1": 8,
    "2": 8,
    "3": 7,
    "4": 7,
    "5": 7,
    "6": 7
}
MAX_HOURS = {
    "Monday": 10,
    "Tuesday": 10,
    "Wednesday": 10,
    "Thursday": 10,
    "Friday": 10
}
MAX_SHIFT = 2
MAX_STUDENTS_PER_DAY = 3
TOTAL_DUTY_HOURS = 70
MAX_5_6_HOURS = 14
THURSDAY_5_LIMIT = 2

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="x1")
x2 = m.addVar(vtype=GRUB.BINARY, name="x2")
x3 = m.addVar(vtype=GRB.BINARY, name="x3")
x4 = m.addVar(vtype=GRB.BINARY, name="x4")
x5 = m.addVar(vtype=GRB.BINARY, name="x5")
x6 = m.addVar(vtype=GRB.BINARY, name="x6")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    6 * x1 + 8 * x2 + 9 * x3 + 5 * x4 + 5 * x5 + 4 * x6,
    GRB.MAXIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 <= MAX_STUDENTS_PER_DAY, "MaxStudentsPerDay")
m.addConstr(x1 * HOURS["1"] + x2 * HOURS["2"] + x3 * HOURS["3"] + x4 * HOURS["4"] + x5 * HOURS["5"] + x6 * HOURS["6"] <= TOTAL_DUTY_HOURS, "TotalDutyHours")
m.addConstr(x1 * MAX_HOURS["Monday"] + x2 * MAX_HOURS["Tuesday"] + x3 * MAX_HOURS["Wednesday"] + x4 * MAX_HOURS["Thursday"] + x5 * MAX_HOURS["Friday"] + x6 * MAX_HOURS["Saturday"] <= MAX_STUDENTS_PER_DAY * MAX_HOURS["Monday"], "MaxHoursPerDay")
m.addConstr(x1 * WAGE["Monday"] + x2 * WAGE["Tuesday"] + x3 * WAGE["Wednesday"] + x4 * WAGE["Thursday"] + x5 * WAGE["Friday"] + x6 * WAGE["Saturday"] <= 1000000, "WageConstraint")
m.addConstr(x1 + x2 + x3 + x4 + x5 + x6 <= MAX_STUDENTS_PER_DAY, "MaxShiftsPerStudent")
m.addConstr(x5 + x6 <= MAX_5_6_HOURS, "Max56Hours")
m.addConstr(x5 <= THURSDAY_5_LIMIT, "Thurs5Limit")

# 6. Optimization and Output
m.optimize()

# Print results for each variable
for v in m.getVars():
    print(f'{v.varName} = {v.x}')
print(f'Optimal Objective Value = {m.objVal}')