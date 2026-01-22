import pulp

# Define the problem
prob = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Define the variables
employees = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10']  # Adjust this list based on the actual number of employees
shifts = [1, 2, 3, 4, 5, 6, 7]  # Shifts correspond to Monday to Sunday
required_employees = {1: 15, 2: 13, 3: 15, 4: 18, 5: 14, 6: 16, 7: 10}

# Binary variables for employee availability
x = pulp.LpVariable.dicts('x', (employees, shifts), cat='Binary')

# Binary variables for employee assignment
y = pulp.LpVariable.dicts('y', employees, cat='Binary')

# Objective function: Minimize the number of employees
prob += pulp.lpSum(y[i] for i in employees), "Total Employees"

# Constraints
for i in employees:
    prob += pulp.lpSum(x[i][j] for j in shifts) == 5, f"Employee_{i}_availability"
    prob += pulp.lpSum(x[i][j] for j in shifts) <= 2, f"Employee_{i}_availability_limit"

for j in shifts:
    prob += pulp.lpSum(x[i][j] for i in employees) >= required_employees[j], f"Shift_{j}_requirement"

# Solve the problem
prob.solve()

# Print the results
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Total Employees: {pulp.value(prob.objective)}")

# Display which employees are assigned to work
for i in employees:
    if y[i].value() > 0:
        print(f"Employee {i} is assigned to work.")