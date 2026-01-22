import pulp

# Define the problem
prob = pulp.LpProblem("Maximize_Bandwidth", pulp.LpMaximize)

# Define the nodes and their connections with bandwidths
nodes = ['A', 'B', 'C', 'D', 'E']
bandwidth_matrix = [
    [0, 90, 85, 0, 65],
    [95, 0, 70, 65, 34],
    [60, 0, 0, 88, 80],
    [67, 30, 25, 0, 84],
    [0, 51, 0, 56, 0]
]

# Define decision variables
x_AC = pulp.LpVariable('x_AC', cat='Binary')
x_CE = pulp.LpVariable('x_CE', cat='Binary')

# Define the objective function
prob += x_AC * min(bandwidth_matrix[0][2], bandwidth_matrix[2][4]) + \
        x_CE * min(bandwidth_matrix[2][4], bandwidth_matrix[4][4]) - \
        x_AC * x_CE * min(bandwidth_matrix[0][2], bandwidth_matrix[2][4])

# Define constraints
prob += x_AC + x_CE == 1, "PathFromAtoEThroughC"

# Solve the problem
prob.solve()

# Print the status of the solution
print(f"Status: {pulp.LpStatus[prob.status]}")

# Extract the maximum bandwidth
max_bandwidth = min(bandwidth_matrix[0][2], bandwidth_matrix[2][4]) if pulp.value(x_AC) == 1 else min(bandwidth_matrix[2][4], bandwidth_matrix[4][4])
print(f"Maximum Bandwidth: {max_bandwidth}")

# Print the values of the decision variables
print(f"x_AC: {pulp.value(x_AC)}, x_CE: {pulp.value(x_CE)}")