def prob_1(color_printers, bw_printers):
    """ 
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Objective function coefficients
    obj = [200, 70]
    
    # Constraints coefficients matrix
    A = [
        [1, 1],  # x + y <= 35
        [1, 0],  # x <= 20
        [0, 1],  # y <= 30
        [-1, 0], # -x >= 0
        [0, -1]  # -y >= 0
    ]
    
    # Constraints right-hand side values
    b = [35, 20, 30, 0, 0]
    
    # Solve the linear programming problem
    from scipy.optimize import linprog
    result = linprog(c=obj, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
    
    # Return the optimal objective value
    return int(result.fun)