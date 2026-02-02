import pulp

# Define the problem
prob = pulp.LpProblem("Employee_Scheduling_Problem", pulp.LpMinimize)

# Define the decision variables
A_i = pulp.LpVariable.dicts("A_i", range(1), lowBound=0, cat='Continuous')
B_i = pulp.LpVariable.dicts("B_i", range(1), lowBound=0, cat='Continuous')
C_i = pulp.LpVariable.dicts("C_i", range(1), lowBound=0, cat='Continuous')
D_i = pulp.LpVariable.dicts("D_i", range(1), lowBound=0, cat='Continuous')
E_i = pulp.LpVariable.dicts("E_i", range(1), lowBound=0, cat='Continuous')
F_i = pulp.LpVariable.dicts("F_i", range(1), lowBound=0, cat='Continuous')
G_i = pulp.LpVariable.dicts("G_i", range(1), lowBound=0, cat='Continuous')
H_i = pulp.LpVariable.dicts("H_i", range(1), lowBound=0, cat='Continuous')

# Define the objective function
prob += pulp.lpSum([A_i[i] for i in range(1)]) + \
        pulp.lpSum([B_i[i] for i in range(1)]) + \
        pulp.lpSum([C_i[i] for i in range(1)]) + \
        pulp.lpSum([D_i[i] for i in range(1)]) + \
        pulp.lpSum([E_i[i] for i in range(1)]) + \
        pulp.lpSum([F_i[i] for i in range(1)]) + \
        pulp.lpSum([G_i[i] for i in range(1)]) + \
        pulp.lpSum([H_i[i] for i in range(1)])

# Define the constraints
prob += pulp.lpSum([A_i[i] for i in range(1)]) + D_i[1] + E_i[1] + F_i[1] + G_i[1] + H_i[1] == 15, "Monday_Constraint"
prob += pulp.lpSum([B_i[i] for i in range(1)]) + D_i[1] + E_i[1] + F_i[1] + G_i[1] + H_i[1] == 13, "Tuesday_Constraint"
prob += pulp.lpSum([C_i[i] for i in range(1)]) + D_i[1] + E_i[1] + F_i[1] + G_i[1] + H_i[1] == 15, "Wednesday_Constraint"
prob += pulp.lpSum([D_i[i] for i in range(1)]) + E_i[1] + F_i[1] + G_i[1] + H_i[1] == 18, "Thursday_Constraint"
prob += pulp.lpSum([E_i[i] for i in range(1)]) + F_i[1] + G_i[1] + H_i[1] == 14, "Friday_Constraint"
prob += pulp.lpSum([F_i[i] for i in range(1)]) + G_i[1] + H_i[1] == 16, "Saturday_Constraint"
prob += pulp.lpSum([G_i[i] for i in range(1)]) + H_i[1] == 10, "Sunday_Constraint"

prob += A_i[1] - B_i[1] <= 7, "Monday_Wednesday_Difference_Constraint"
prob += C_i[1] + D_i[1] >= 3, "Sunday_Monday_Off_Constraint"

# Solve the problem
prob.solve()

# Print the results
print("Status:", pulp.LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total Minimum Employees Used =", pulp.value(prob.objective))