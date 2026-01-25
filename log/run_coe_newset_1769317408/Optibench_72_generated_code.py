import numpy as np
from scipy.optimize import linprog

# Coefficients of the objective function (negative because linprog minimizes)
c = [-40, -70, -100, -50, -90]  # Negative sign for maximization

# Coefficients of the inequality constraints
A = [
    [1, 1, 1, 1, 1],  # Total number of development teams available
    [1, -2, 0, 0, 0],  # AppX must have at least twice as many development teams as AppY
    [60, 80, 100, 70, 90],  # Marketing cost budget
    [1, 1, 1, 1, 0],  # At least two teams are required to be assigned to the AppX development project
    [1, 1, 1, 1, 0],  # Total number of development teams assigned to AppX, AppY, AppW, and AppV combined must not exceed 10 teams
    [0, 0, 1, 0, 1],  # Total number of development teams assigned to AppZ and AppV combined must not exceed 28 teams
    [0, 0, 0, 0, 1]  # Each product has at least one team working on it
]

# Right-hand side values of the inequality constraints
b = [30, 2, 2500000, 2, 10, 28, 1]

# Bounds for each variable (number of development teams)
x_bounds = [(1, None)] * 5  # Each product must have at least one team

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Extract the solution
solution = result.x
average_net_profit = result.fun

print(f"Solution: {solution}")
print(f"Average Net Profit: {average_net_profit}")