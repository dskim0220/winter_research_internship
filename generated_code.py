import numpy as np
from scipy.optimize import linprog

def prob_1(color_printers, bw_printers):
    """
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Coefficients of the objective function to minimize (negative because linprog minimizes by default)
    c = [-200, -70]  # Negative coefficients to maximize profit

    # Coefficients matrix for the inequality constraints
    A = [
        [1, 1],  # x + y <= 35
        [1, 0],  # x <= 20
        [0, 1],  # y <= 30
        [-1, 0], # x >= 0
        [0, -1]  # y >= 0
    ]

    # Right-hand side values for the inequality constraints
    b = [35, 20, 30, 0, 0]

    # Bounds for x and y (both must be non-negative)
    bounds = [(0, None), (0, None)]

    # Solve the linear programming problem
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # Return the optimal objective value (profit)
    return -res.fun  # Negate again to get the actual profit

# Example usage:
color_printers = 15
bw_printers = 20
optimal_profit = prob_1(color_printers, bw_printers)
print(f"Optimal Profit: ${optimal_profit:.2f}")