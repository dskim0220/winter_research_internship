import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
EMPLOYEES_REQUIRED = {day: value for day, value in ("Monday", 15), ("Tuesday", 13), ("Wednesday", 15), ("Thursday", 18), ("Friday", 14), ("Saturday", 16), ("Sunday", 10).items()}
MIN_DIFFERENCE = 7
SUNDAY_MONDAY_PAIR = 3

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x = {}
y = {}

for day in EMPLOYEES_REQUIRED.keys():
    for group in ["Group1", "Group2", "Group3", "Group4", "Group5"]:
        x[day, group] = m.addVar(vtype=GRB.BINARY, name=f"x_{day}_{group}")
        y[day, group] = m.addVar(name=f"y_{day}_{group}")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(
    0 * x["Monday", "Group1] + 0 * x["Monday", "Group2] + 0 * x["Monday", "Group3"] + 0 * x["Monday", "Group4"] + 0 * x["Monday", "Group5"] +
    0 * x["Tuesday", "Group1] + 124 * x["Tuesday", "Group1] + 109 * x["Tuesday", "Group2] + 12100 * x["Tuesday", "Group3] + 12100 * x["Tuesday", "Group4"] + 12100 * x["Tuesday", "Group5"] +
    0 * x["Wednesday", "Group1] + 12100 * x["Wednesday", "Group2] + 12100 * x["Wednesday", "Group3"] + 12100 * x["Wednesday", "Group4"] + 12100 * x["Wednesday", "Group5"] +
    0 * x["Thursday", "Group1] + 0 * x["Thursday", "Group2] + 0 * x["Thursday", "Group3"] + 12100 * x["Thursday", "Group4"] + 12100 * x["Thursday", "Group5"] +
    0 * x["Friday", "Group1] + 0 * x["Friday", "Group2] + 0 * x["Friday", "Group3"] + 0 * x["Friday", "Group4"] + 12100 * x["Friday", "Group5"] +
    0 * x["Saturday", "Group1] + 0 * x["Saturday", "Group2"] + 0 * x["Saturday", "Group3"] + 0 * x["Saturday", "Group4"] + 0 * x["Saturday", "Group5"] +
    0 * x["Sunday", "Group1] + 0 * x["Sunday", "Group2"] + 0 * x["Sunday", "Group3"] + 0 * x["Sunday", "Group4"] + 0 * x["Sunday", "Group5"],
    GRB.MINIMIZE
)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
m.addConstr(
    gp.quicksum(x[day, "Group1"] for day in ["Monday", "Wednesday"]) <= x["Monday", "Group1"] + x["Wednesday", "Group1"],
    "shift_constraint_1"
)
m.addConstr(
    gp.quicksum(x[day, "Group1"] for day in ["Sunday", "Monday"]) >= y["Monday", "Group1"] + y["Tuesday", "Group1"] + y["Wednesday", "Group1"] + y["Thursday", "Group1"] + y["Friday", "Group1"],
    "shift_constraint_2"
)
m.addConstr(
    gp.quicksum(x[day, "Group1"] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]) == 1,
    "group_constraint"
)
m.addConstr(
    gp.quicksum(y[day, "Group1"] for day in EMPLOYEES_REQUIRED.keys()) == EMPLOYEES_REQUIRED["Monday"] + EMPLOYEES_REQUIRED["Tuesday"] + EMPLOYEES_REQUIRED["Wednesday"] + EMPLOYEES_REQUIRED["Thursday"] + EMPLOYEES_REQUIRED["Friday