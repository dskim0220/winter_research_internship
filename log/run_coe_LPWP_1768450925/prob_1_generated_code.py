import gurobipy as gp
from gurobipy import GRB

def prob_1(color_printers, bw_printers):
    """
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Create a new model
    m = gp.Model("printer_production")
    
    # Create variables
    x = m.addVar(name="color_printers")  # Number of color printers
    y = m.addVar(name="bw_printers")     # Number of black and white printers
    
    # Set objective
    m.setObjective(200 * x + 70 * y, GRB.MAXIMIZE)
    
    # Add constraints
    m.addConstr(x <= 20, "color_team_constraint")
    m.addConstr(y <= 30, "bw_team_constraint")
    m.addConstr(x + y <= 35, "machine_constraint")
    
    # Optimize model
    m.optimize()
    
    # Return the optimal objective value
    obj = m.objVal
    return obj