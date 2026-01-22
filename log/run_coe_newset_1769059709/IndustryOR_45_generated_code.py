from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger

# Define the problem
prob = LpProblem("Student_Duty_Planner", LpMinimize)

# Define the wage rates for each student
wages = {
    1: 10.0,
    2: 10.0,
    3: 9.9,
    4: 9.8,
    5: 10.8,
    6: 11.3
}

# Define the binary variables
x = {(i, j): LpVariable(f"x_{i}{j}", cat='Binary') for i in range(1, 7) for j in range(1, 6)}

# Define the binary variables for the constraints
y = {i: LpVariable(f"y_{i}", cat='Binary') for i in range(1, 7)}
z = {i: LpVariable(f"z_{i}", cat='Binary') for i in range(1, 7)}

# Objective function: Minimize total wage
prob += lpSum([wages[i] * x[(i, j)] for i in range(1, 7) for j in range(1, 6)])

# Constraints
# Each student works at most 2 shifts per week
for i in range(1, 7):
    prob += lpSum([x[(i, j)] for j in range(1, 6)]) <= 2 * z[i]

# Each student works at least 7 hours per week
for i in range(1, 7):
    prob += lpSum([7 * x[(i, j)] for j in range(1, 6)]) >= 7 * y[i]

# Each student works at least 8 hours per week
for i in range(1, 7):
    prob += lpSum([8 * x[(i, j)] for j in range(1, 6)]) >= 8 * y[i]

# No more than 3 students can be scheduled for duty each day
for j in range(1, 6):
    prob += lpSum([x[(i, j)] for i in range(1, 7)]) <= 3

# Each student must work at least one shift in the week
for i in range(1, 7):
    prob += lpSum([x[(i, j)] for j in range(1, 6)]) >= 1 * y[i]

# Each student works exactly 2 shifts in the week if z_i = 1
for i in range(1, 7):
    prob += lpSum([x[(i, j)] for j in range(1, 6)]) == 2 * z[i]

# Each student works at least one shift in the week if y_i = 1
for i in range(1, 7):
    prob += lpSum([x[(i, j)] for j in range(1, 6)]) >= 1 * y[i]

# Solve the problem
prob.solve()

# Print the status of the solution
print("Status:", LpProblem.status[prob.status])

# Print the results
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Calculate the total cost
total_cost = 0
for i in range(1, 7):
    for j in range(1, 6):
        if x[(i, j)].varValue == 1:
            total_cost += wages[i] * 1

print("Total Cost:", total_cost)