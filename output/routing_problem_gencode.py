import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
N = 12100  # Number of input/output ports
L_E = 100  # Unit length of a grid edge
W = 1000  # Penalty cost per turn
MIN_PERPENDICULAR_DISTANCE = 1210  # Minimum perpendicular distance between paths
TOTAL_PATH_LENGTH = N  # Sum of lengths of all paths
TOTAL_TURN_COUNT = N  # Sum of turn counts of all paths

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)
x1 = m.addVar(vtype=GRB.BINARY, name="x1")
x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2")

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)
m.setObjective(12100 * x1 + 1000 * x2, GRB.MINIMIZE)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
# Ensure unit consistency (e.g., 1,210 tons -> 12100 in 100kg units)
m.addConstr(x1 + x2 <= 1, "Path_Disjointness")
m.addConstr(x1 + x2 <= 1, "Non_Crossing")
m.addConstr(100 - 100 <= 45, "Movement_Limitations")  # Simplified constraint for demonstration
m.addConstr(x2 <= 1, "Curvature_Constraint")
m.addConstr(12100 - 12100 <= 0, "Minimum_Perpendicular_Distance")  # Simplified constraint for demonstration

# 6. Optimization and Output
m.optimize()
#... (Print results for each variable)