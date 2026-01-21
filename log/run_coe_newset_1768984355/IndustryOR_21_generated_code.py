import pulp

def optimize_table_order():
    """
    This function optimizes the order of dining tables from three suppliers A, B, and C.
    """
    # Create a LP problem
    prob = pulp.LpProblem("Table_Order_Problem", pulp.LpMinimize)

    # Define decision variables
    x_A = pulp.LpVariable('x_A', lowBound=0, cat='Integer')
    x_B = pulp.LpVariable('x_B', lowBound=0, cat='Integer')
    x_C = pulp.LpVariable('x_C', lowBound=0, cat='Integer')

    # Objective function
    prob += 120 * x_A + 110 * x_B + 100 * x_C, "Total Cost"

    # Constraints
    prob += x_A * 20 + x_B * 15 + x_C * 15 >= 150, "Minimum_Tables_Constraint"
    prob += x_A * 20 + x_B * 15 + x_C * 15 <= 600, "Maximum_Tables_Constraint"
    prob += x_A >= 30, "Supplier_A_Minimum_Constraint"
    prob += x_B >= x_C, "Supplier_B_Supplier_C_Constraint"
    prob += x_A <= 600 / 20, "Supplier_A_Max_Constraint"
    prob += x_B <= 600 / 15, "Supplier_B_Max_Constraint"
    prob += x_C <= 600 / 15, "Supplier_C_Max_Constraint"

    # Solve the problem
    status = prob.solve()

    # Print results
    print(f"Status: {pulp.LpStatus[status]}")
    print(f"Optimal Total Cost: ${pulp.value(prob.objective)}")
    print(f"Number of Orders from Supplier A: {int(pulp.value(x_A))}")
    print(f"Number of Orders from Supplier B: {int(pulp.value(x_B))}")
    print(f"Number of Orders from Supplier C: {int(pulp.value(x_C))}")

# Run the optimization
optimize_table_order()