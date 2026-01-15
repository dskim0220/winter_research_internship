import pulp

def prob_1(color_printers, bw_printers):
    """
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Create a LP maximization problem
    prob = pulp.LpProblem("Printer_Profit", pulp.LpMaximize)

    # Decision variables
    x = pulp.LpVariable("color_printers", lowBound=0, cat='Continuous')
    y = pulp.LpVariable("bw_printers", lowBound=0, cat='Continuous')

    # Objective function
    prob += 200 * x + 70 * y, "Total_Profit"

    # Constraints
    prob += x <= 20, "Color_Production_Limit"
    prob += y <= 30, "BW_Production_Limit"
    prob += x + y <= 35, "Machine_Limit"

    # Solve the problem
    prob.solve()

    # Retrieve the optimal solution
    obj = pulp.value(prob.objective)
    
    return int(obj)

# Example usage
print(prob_1(20, 30))  # This will print the maximum profit