import numpy as np
from scipy.optimize import linprog

# Coefficients of the objective function (we need to maximize profit)
c = [200, 70]

# Coefficients matrix for the inequality constraints
A = [
    [1, 1],  # A + B <= 35
    [1, 0],  # A <= 20
    [0, 1],  # B <= 30
    [-1, 0], # A >= 0
    [0, -1]  # B >= 0
]

# Right-hand side values for the constraints
b = [35, 20, 30, 0, 0]

# Bounds for the variables (A >= 0, B >= 0)
x0_bounds = (0, None)
x1_bounds = (0, None)

# Solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')

# Calculate the maximum profit
max_profit = res.fun

print(f"Optimal number of color printers: {res.x[0]}")
print(f"Optimal number of black and white printers: {res.x[1]}")
print(f"Maximum profit: ${max_profit}")