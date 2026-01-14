from pulp import LpProblem, LpMaximize, LpVariable, lpSum, Gurobi

def prob_1(color_printers, bw_printers):
    """
    Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers
    
    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Create a new Gurobi model
    model = Gurobi.Model("printer_production")

    # Define decision variables
    x = model.addVar(lb=0, ub=color_printers, name='color_printers')  # Number of color printers
    y = model.addVar(lb=0, ub=bw_printers, name='bw_printers')       # Number of black and white printers

    # Define the objective function
    model.setObjective(200 * x + 70 * y, sense=LpMaximize)

    # Add constraints
    model.addConstr(x + y <= 35, name='machine_capacity')
    model.addConstr(x <= 20, name='color_printer_capacity')
    model.addConstr(y <= 30, name='bw_printer_capacity')

    # Solve the model
    model.solve()

    # Retrieve the optimal solution
    obj_value = model.objective.getValue()
    color_printers_optimal = x.varValue
    bw_printers_optimal = y.varValue

    return int(obj_value)

# Example usage
print(prob_1(20, 30))