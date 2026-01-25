import pulp

# Define the number of employees and days
n = 10  # Number of employees (can be adjusted)
m = 10  # Number of possible schedules (can be adjusted)

# Create a problem instance
prob = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(1, n+1) for j in range(1, 6)], cat='Binary')  # Employee works from Monday to Friday including day j
y = pulp.LpVariable.dicts("y", [k for k in range(1, m+1)], cat='Binary')  # Employee has both Sunday and Monday off consecutively

# Objective function: minimize the total number of employees used
prob += pulp.lpSum([x[i][j] for i in range(1, n+1) for j in range(1, 6)]) + pulp.lpSum([y[k] for k in range(1, m+1)])

# Constraints
# Constraint 1: Each employee works exactly one five-day shift
for i in range(1, n+1):
    prob += pulp.lpSum([x[i][j] for j in range(1, 6)]) == 1

# Constraint 2: Employee availability constraints
for j in range(1, 6):
    prob += pulp.lpSum([x[i][j] for i in range(1, n+1)]) == 15 if j == 1 else 13 if j == 2 else 15 if j == 3 else 18 if j == 4 else 14 if j == 5 else 10

# Constraint 3: Shift continuity constraint
for i in range(1, n+1):
    for j in range(1, 4):
        prob += x[i][j] + x[i][j+1] - x[i][j+2] - x[i][j+3] - x[i][j+4] == 0

# Constraint 4: Shift rotation constraint
prob += pulp.lpSum([x[i][1] for i in range(1, n+1)]) - pulp.lpSum([x[i][3] for i in range(1, n+1)]) <= 7
prob += pulp.lpSum([x[i][3] for i in range(1, n+1)]) - pulp.lpSum([x[i][1] for i in range(1, n+1)]) <= 7

# Constraint 5: Sunday and Monday off constraint
for k in range(1, m+1):
    prob += y[k] <= x[k][1]
    prob += y[k] <= x[k][2]

# Constraint 6: At least three employees with Sunday and Monday off
prob += pulp.lpSum([y[k] for k in range(1, m+1)]) >= 3

# Solve the problem
prob.solve()

# Print the results
print("Status:", pulp.LpStatus[prob.status])
print("Total number of employees used:", pulp.value(prob.objective))

# Output the schedule
schedule = {}
for i in range(1, n+1):
    for j in range(1, 6):
        if x[i][j].varValue == 1:
            schedule[i] = j

print("Schedule:")
for k in range(1, m+1):
    print(f"Employee {k}: {schedule[k]}")