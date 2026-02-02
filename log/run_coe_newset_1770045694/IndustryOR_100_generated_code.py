import pulp

# Data for the bandwidth table
bandwidth_table = {
    ('A', 'B'): 90,
    ('A', 'C'): 85,
    ('A', 'E'): 65,
    ('B', 'C'): 70,
    ('B', 'D'): 65,
    ('B', 'E'): 34,
    ('C', 'D'): 25,
    ('C', 'E'): 80,
    ('D', 'E'): 84
}

# Create the problem
prob = pulp.LpProblem("Bandwidth_Maximization", pulp.LpMaximize)

# Define the variables
x_AC = pulp.LpVariable('x_AC', cat='Binary')
x_CE = pulp.LpVariable('x_CE', cat='Binary')
b_AC = pulp.LpVariable('b_AC', lowBound=0)
b_CE = pulp.LpVariable('b_CE', lowBound=0)

# Define the objective function
prob += b_AC + b_CE, 'Total_Bandwidth'

# Define the constraints
prob += x_AC + x_CE == 1, 'Path_Constraint'
prob += b_AC + b_CE >= 100, 'Bandwidth_Constraint'

# Solve the problem
prob.solve()

# Print the status of the solution
print(f"Status: {pulp.LpStatus[prob.status]}")

# Print the results
print(f"x_AC = {pulp.value(x_AC)}, x_CE = {pulp.value(x_CE)}")
print(f"b_AC = {pulp.value(b_AC)}, b_CE = {pulp.value(b_CE)}")
print(f"Maximum Bandwidth = {pulp.value(prob.objective)}")