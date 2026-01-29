import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
EMPLOYEES_REQUIRED = {
    "Monday": 15,
    "Tuesday": 13,
    "Wednesday": 15,
    "Thursday": 18,
    "Friday": 14,
    "Saturday": 16,
    "Sunday": 10
}
MIN_SUNDAY_MONDAY_PAIR = 3
DIFFERENCE_LIMIT = 7

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
EmployeeSchedule = m.addVars(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], vtype=GRB.BINARY)
ShiftStartDay = m.addVars(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], vtype=GRB.CONTINUOUS)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(gp.quicksum(EmployeeSchedule[day] for day in EmployeeSchedule), GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstrs((gp.quicksum(EmployeeSchedule[day] for day in ["Monday", day]) == EMPLOYEERS_REQUIRED[day] for day in EmployeeSchedule.keys()), name="EmploymentRequirement")
m.addConstr(gp.quicksum(EmployeeSchedule[day] for day in ["Sunday", "Monday"]) >= MIN_SUNDAY_MONDAY_PAIR, name="SundayMondayPairConstraint")

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)