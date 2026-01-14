def prob_1(color_printers, bw_printers):
    """ 
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    from scipy.optimize import linprog

    # Coefficients for the objective function (negated because linprog minimizes)
    c = [-200, -70]

    # Coefficients for the inequality constraints
    A = [[1, 1], [1, 0], [0, 1]]
    b = [35, 20, 30]

    # Bounds for the variables
    x_bounds = (0, None)
    y_bounds = (0, None)

    # Solve the linear programming problem
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

    # Return the optimal objective value (profit)
    return -res.fun