def prob_1(C, B):
    """Args:
        C: an integer representing the number of color printers
        B: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Constraints
    if C + B > 35 or C > 20 or B > 30 or C < 0 or B < 0:
        return -1  # Return -1 if any constraint is violated

    # Objective function
    obj = 200 * C + 70 * B

    return obj