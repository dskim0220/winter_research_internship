import numpy as np
from scipy.optimize import linprog

def prob_10(A, B, constraint1, constraint2, constraint3):
    """
    Args:
        A: an integer, kg of fertilizer A
        B: an integer, kg of fertilizer B
        constraint1: an integer, constraint 1 value (minimum 220 units of nitrogen)
        constraint2: an integer, constraint 2 value (minimum 160 units of phosphoric acid)
        constraint3: an integer, constraint 3 value (no more than 350 units of vitamin A)
    Returns:
        obj: an integer, amount of vitamin D
    """
    # Coefficients of the objective function (to minimize vitamin D)
    c = [9, 9]  # Coefficients for vitamin A and vitamin D
    
    # Coefficients matrix for the inequality constraints
    A_ub = [[13, 8], [5, 14], [6, 6]]  # Constraints for nitrogen, phosphoric acid, and vitamin A
    
    # Right-hand side of the inequality constraints
    b_ub = [constraint1, constraint2, -constraint3]
    
    # Bounds for variables A and B (non-negative)
    x0_bounds = (0, None)
    x1_bounds = (0, None)
    
    # Solve the linear programming problem
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[x0_bounds, x1_bounds], method='highs')
    
    # The minimum amount of vitamin D
    obj = res.fun
    
    return obj

# Example usage
A = 10
B = 10
constraint1 = 220
constraint2 = 160
constraint3 = 350

result = prob_10(A, B, constraint1, constraint2, constraint3)
print(f"The minimum amount of vitamin D is {result} units.")