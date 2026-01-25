import numpy as np
from scipy.optimize import linprog

# Coefficients for the objective function (minimize)
c = [-120, -110, -100]  # Cost coefficients for Supplier A, Supplier B, and Supplier C respectively

# Coefficients for the inequality constraints
A = [
    [20, 0, 0],  # 20x_A <= 600
    [0, 15, 0],  # 15x_B <= 600
    [0, 0, 15],  # 15x_C <= 600
    [1, -1, 0],  # x_A - x_B >= 0 (Supplier B must be ordered if Supplier A is ordered)
    [1, 0, -1],  # x_A - x_C >= 0 (Supplier C must be ordered if Supplier A is ordered)
    [20, 15, 0], # 20x_A + 15x_B >= 25 (Supplier A and B together must be at least 25)
    [20, 0, 15], # 20x_A + 15x_C >= 25 (Supplier A and C together must be at least 25)
    [20, 0, 0],  # 20x_A + 15x_B >= 30 (Supplier A and B together must be at least 30)
    [1, 1, 1],   # x_A + x_B + x_C >= 7 (total orders must be at least 7)
    [20, 0, 0],  # 20x_A <= 60 (total tables from Supplier A cannot exceed 60)
]

b = [
    600,        # 20x_A <= 600
    600,        # 15x_B <= 600
    600,        # 15x_C <= 600
    0,          # x_A - x_B >= 0
    0,          # x_A - x_C >= 0
    25,         # 20x_A + 15x_B >= 25
    25,         # 20x_A + 15x_C >= 25
    30,         # 20x_A + 15x_B >= 30
    7,          # x_A + x_B + x_C >= 7
    3,          # 20x_A <= 60
]

# Bounds for the variables (non-negative integers)
x_bounds = [(0, None), (0, None), (0, None)]

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Extract the solution
x_A, x_B, x_C = result.x
total_cost = -result.fun  # Since linprog returns the negative of the objective function value

print(f"Number of orders from Supplier A: {int(x_A)}")
print(f"Number of orders from Supplier B: {int(x_B)}")
print(f"Number of orders from Supplier C: {int(x_C)}")
print(f"Total cost: ${-total_cost:.2f}")