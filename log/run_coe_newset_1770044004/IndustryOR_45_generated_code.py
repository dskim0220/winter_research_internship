import pulp

# Define the data
students = ['1', '2', '3', '4', '5', '6']
wages = [10.0, 10.0, 9.9, 9.8, 10.8, 11.3]
monday_hours = [6, 0, 4, 5, 3, 0]
tuesday_hours = [0, 8, 8, 5, 0, 6]
wednesday_hours = [6, 9, 3, 6, 5, 0]
thursday_hours = [0, 0, 0, 0, 8, 6]
friday_hours = [7, 0, 5, 4, 0, 5]

# Create the problem
prob = pulp.LpProblem("University_Duty_Schedule", pulp.LpMinimize)

# Define binary variables
x_ij = pulp.LpVariable.dicts("x_ij", [(s, d) for s in students for d in range(1, 6)], cat='Binary')

# Define continuous variables
y_i = pulp.LpVariable.dicts("y_i", students, lowBound=0, upBound=None, cat='Continuous')

# Objective function: minimize total gross pay
prob += pulp.lpSum([y_i[s] * wages[int(s)-1] for s in students]), "Total_Gross_Pay"

# Constraints
# 1. Each student works exactly 2 shifts per week
for s in students:
    prob += pulp.lpSum([x_ij[s, d] for d in range(1, 6)]) == 2, f"Shift_Constraint_{s}"

# 2. Each undergraduate works at least 8 hours per week
for u in ['1', '2', '3', '4']:
    prob += pulp.lpSum([y_i[u] * monday_hours[d] for d in range(1, 6)] + 
                       [y_i[u] * tuesday_hours[d] for d in range(1, 6)] + 
                       [y_i[u] * wednesday_hours[d] for d in range(1, 6)] + 
                       [y_i[u] * thursday_hours[d] for d in range(1, 6)] + 
                       [y_i[u] * friday_hours[d] for d in range(1, 6)]) >= 8, f"Undergraduate_Hours_{u}"

# 3. Each graduate student works at least 7 hours per week
for g in ['5', '6']:
    prob += pulp.lpSum([y_i[g] * monday_hours[d] for d in range(1, 6)] + 
                       [y_i[g] * tuesday_hours[d] for d in range(1, 6)] + 
                       [y_i[g] * wednesday_hours[d] for d in range(1, 6)] + 
                       [y_i[g] * thursday_hours[d] for d in range(1, 6)] + 
                       [y_i[g] * friday_hours[d] for d in range(1, 6)]) >= 7, f"Graduate_Hours_{g}"

# 4. No more than 3 students can be scheduled for duty each day
for d in range(1, 6):
    prob += pulp.lpSum([x_ij[s, d] for s in students]) <= 3, f"Daily_Shift_Limit_{d}"

# 5. Total duty hours of all undergraduates and graduate students are 70 hours
prob += pulp.lpSum([y_i[s] * monday_hours[d] for s in students for d in range(1, 6)] + 
                   [y_i[s] * tuesday_hours[d] for s in students for d in range(1, 6)] + 
                   [y_i[s] * wednesday_hours[d] for s in students for d in range(1, 6)] + 
                   [y_i[s] * thursday_hours[d] for s in students for d in range(1, 6)] + 
                   [y_i[s] * friday_hours[d] for s in students for d in range(1, 6)]) == 70, "Total_Duty_Hours"

# 6. Sum of duty hours of student 5 and 6 can not exceed 14
prob += pulp.lpSum([y_i['5'] * monday_hours[d] + y_i['5'] * tuesday_hours[d] + y_i['5'] * wednesday_hours[d] + 
                    y_i['5'] * thursday_hours[d] + y_i['5'] * friday_hours[d] +
                    y_i['6'] * monday_hours[d] + y_i['6'] * tuesday_hours[d] + y_i['6'] * wednesday_hours[d] + 
                    y_i['6'] * thursday_hours[d] + y_i['6'] * friday_hours[d] for d in range(1, 6)]) <= 14, "Student_5_and_6_Hours"

# 7. Student 5 must work less than 2 hours on Thursday
prob += pulp.lpSum([y_i['5'] * thursday_hours[d] for d in range(1, 6)]) <= 1, "Student_5_Thursday_Hours"

# Solve the problem
status = prob.solve()

# Print the results
print(f"Status: {pulp.LpStatus[status]}")
print(f"Total Gross Pay: {pulp.value(prob.objective)}")

# Display the schedule
for s in students:
    print(f"Student {s}:")
    for d in range(1, 6):
        if pulp.value(x_ij[s, d]) == 1:
            print(f"  Day {d}: On Duty")
        else:
            print(f"  Day {d}: Off Duty")
    print()