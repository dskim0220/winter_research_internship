import gurobipy as gp
from gurobipy import GRB

def optimize_table_order():
    # Create a new model
    m = gp.Model("table_order")
    
    # Add decision variables
    x_A = m.addVar(vtype=GRB.INTEGER, name="xA")  # Number of orders from Supplier A
    x_B = m.addVar(vtype=GRB.INTEGER, name="xB")  # Number of orders from Supplier B
    x_C = m.addVar(vtype=GRB.INTEGER, name="xC")  # Number of orders from Supplier C
    
    # Set objective function
    m.setObjective(120 * x_A + 110 * x_B + 100 * x_C, GRB.MINIMIZE)
    
    # Add constraints
    m.addConstr(20 * x_A + 15 * x_B + 15 * x_C >= 150, "min_tables")
    m.addConstr(20 * x_A + 15 * x_B + 15 * x_C <= 600, "max_tables")
    m.addConstr(x_B >= 30, "min_B_given_A")
    m.addConstr(x_C >= 1, "min_C_given_B")
    
    # Optimize the model
    try:
        m.optimize()
        
        # Check if the model has been solved
        if m.status == GRB.OPTIMAL:
            print(f"Optimal Solution Found:")
            print(f"x_A = {x_A.x}")
            print(f"x_B = {x_B.x}")
            print(f"x_C = {x_C.x}")
            print(f"Total Cost = {m.objVal}")
        elif m.status == GRB.INFEASIBLE:
            print("The model is infeasible.")
        elif m.status == GRB.INF_OR_UNBD:
            print("The model is unbounded.")
        elif m.status == GRB.UNBOUNDED:
            print("The model is unbounded.")
        elif m.status == GRB.OPTIMAL:
            print("The model is optimal.")
        else:
            print("The model status is unknown.")
    except gp.GurobiError as e:
        print('Error code '+str(e.errno)+' : '+str(e))
    except AttributeError:
        print('Model is not optimized/feasible.')

# Call the function
optimize_table_order()