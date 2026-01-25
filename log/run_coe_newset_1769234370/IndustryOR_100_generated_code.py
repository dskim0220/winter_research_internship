import pulp

# Define the problem
prob = pulp.LpProblem("Network_Bandwidth_Problem", pulp.LpMaximize)

# Define the nodes and their connections
nodes = ['A', 'B', 'C', 'D', 'E']
bandwidth_matrix = [
    [0, 90, 85, 0, 65],
    [95, 0, 70, 65, 34],
    [60, 0, 0, 88, 80],
    [67, 30, 25, 0, 84],
    [0, 51, 0, 56, 0]
]

# Define the variables
x = pulp.LpVariable.dicts('x', [(i, j) for i in nodes for j in nodes], lowBound=0, upBound=1, cat='Binary')
b = pulp.LpVariable.dicts('b', [(i, j) for i in nodes for j in nodes], lowBound=0, cat='Continuous')

# Define the objective function
prob += pulp.lpSum([b[(i, j)] for i in nodes for j in nodes]), "Maximize Bandwidth"

# Define the constraints
# Link constraint: A -> E must pass through C
prob += x[('A', 'C')] + x[('C', 'E')] == 1, "Link_ACE"

# Bandwidth constraint: Total bandwidth of the path A -> C -> E must be at least 100
prob += b[('A', 'C')] + b[('C', 'E')] >= 100, "BandwidthConstraint"

# Efficiency penalty constraints
prob += b[('A', 'B')] * 0.9 <= b[('A', 'E')], "EfficiencyPenalty_AB"
prob += b[('D', 'E')] * 0.96 <= b[('A', 'E')], "EfficiencyPenalty_DE"

# Solve the problem
prob.solve()

# Print the results
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Maximum Bandwidth: {pulp.value(prob.objective)}")

# Display the solution
for i in nodes:
    for j in nodes:
        if x[i, j].value() == 1:
            print(f"Link from {i} to {j} is established with bandwidth {b[i, j].value()}")