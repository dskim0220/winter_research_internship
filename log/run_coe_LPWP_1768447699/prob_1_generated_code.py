def prob_1(color_printers, bw_printers):
    """
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    import gurobipy as gp
    from gurobipy import GRB

    # Create a new model
    m = gp.Model("printer_production")

    # Create variables
    x = m.addVar(name="color_printers")
    y = m.addVar(name="bw_printers")

    # Set objective
    m.setObjective(200 * x + 70 * y, GRB.MAXIMIZE)

    # Add constraints
    m.addConstr(x <= 20, "color_team_constraint")
    m.addConstr(y <= 30, "bw_team_constraint")
    m.addConstr(x + y <= 35, "machine_constraint")

    # Optimize model
    m.optimize()

    # Check if solution exists
    if m.status == GRB.Status.OPTIMAL:
        obj = m.objVal
    else:
        obj = 1e9

    return int(obj)