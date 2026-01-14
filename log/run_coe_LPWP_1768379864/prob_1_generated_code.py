from scipy.optimize import linprog

# Coefficients for the objective function (negative because linprog minimizes)
c = [-200, -70]

# Coefficients for the inequality constraints
A = [
    [1, 1],  # color printers + black and white printers <= 35
    [1, -1],  # color printers - black and white printers <= 0
    [1, 0],   # color printers <= 20
    [0, 1]    # black and white printers <= 30
]

# Right-hand side values for the inequality constraints
b = [35, 0, 20, 30]

# Bounds for the variables (non-negative)
x0_bounds = (0, None)
x1_bounds = (0, None)

# Solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')

# The optimal solution
optimal_color_printers = res.x[0]
optimal_bw_printers = res.x[1]
optimal_profit = -res.fun  # Convert back to positive profit

# Return the optimal profit
def prob_1(color_printers, bw_printers):
    obj = optimal_profit
    return obj

# Final code
prob_1(optimal_color_printers, optimal_bw_printers)