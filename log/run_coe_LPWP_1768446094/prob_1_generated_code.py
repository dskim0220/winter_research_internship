def prob_1(color_printers, bw_printers):
    """Args:
        color_printers: an integer representing the number of color printers
        bw_printers: an integer representing the number of black and white printers

    Returns:
        obj: an integer representing the optimal objective value (profit)
    """
    # Objective function: Maximize profit
    obj = 200 * color_printers + 70 * bw_printers
    
    # Constraints
    constraints = [
        color_printers <= 20,  # Color printer team constraint
        bw_printers <= 30,     # Black and white printer team constraint
        color_printers + bw_printers <= 35  # Paper tray installing machine constraint
    ]
    
    # Check if the solution satisfies all constraints
    if all(constraints):
        return obj
    else:
        return -1  # Return -1 if the solution does not satisfy constraints

# Example usage:
# Assuming we want to find the maximum profit, we need to solve this linear programming problem.
# We can use a solver like PuLP or CVXPY to find the optimal values of color_printers and bw_printers.
from pulp import LpProblem, LpMaximize, LpVariable

# Create a LP problem
prob = LpProblem("Printer_Profit", LpMaximize)

# Decision variables
color_printers = LpVariable('color_printers', lowBound=0, cat='Continuous')
bw_printers = LpVariable('bw_printers', lowBound=0, cat='Continuous')

# Objective function
prob += 200*color_printers + 70*bw_printers, "Total Profit"

# Constraints
prob += color_printers <= 20, "Color Printer Constraint"
prob += bw_printers <= 30, "BW Printer Constraint"
prob += color_printers + bw_printers <= 35, "Machine Constraint"

# Solve the problem
status = prob.solve()

# Print the results
if status == 1:
    print(f"Optimal Solution Found: Color Printers = {value(color_printers)}, BW Printers = {value(bw_printers)}")
    print(f"Maximum Profit = {value(prob.objective)}")
else:
    print("No feasible solution found.")