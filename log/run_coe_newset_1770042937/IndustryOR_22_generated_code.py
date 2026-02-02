import pulp

# Define the problem
prob = pulp.LpProblem("Product_Production_Problem", pulp.LpMaximize)

# Define decision variables
x1 = pulp.LpVariable('x1', lowBound=20, cat='Integer')  # Units of A1
x2 = pulp.LpVariable('x2', lowBound=20, cat='Integer')  # Units of A2
x3 = pulp.LpVariable('x3', lowBound=16, cat='Integer')  # Units of A3
y1 = pulp.LpVariable('y1', cat='Binary')               # Activation of A1 production line
y2 = pulp.LpVariable('y2', cat='Binary')               # Activation of A2 production line
y3 = pulp.LpVariable('y3', cat='Binary')               # Activation of A3 production line

# Objective function: Maximize total revenue
prob += 124 * x1 + 109 * x2 + 115 * x3, "Total_Revenue"

# Constraints
# Production capacity constraint
prob += x1 + x2 + x3 <= 121, "Production_Capacity_Constraint"

# Maximum demand constraints
prob += x1 <= 53, "Max_Demand_A1"
prob += x2 <= 45, "Max_Demand_A2"
prob += x3 <= 54, "Max_Demand_A3"

# Minimum production batch constraints
prob += x1 >= 20, "Min_Batch_A1"
prob += x2 >= 20, "Min_Batch_A2"
prob += x3 >= 16, "Min_Batch_A3"

# Activation cost constraints
prob += 170000 * y1 <= 170000, "Activation_Cost_A1"
prob += 150000 * y2 <= 150000, "Activation_Cost_A2"
prob += 100000 * y3 <= 100000, "Activation_Cost_A3"

# Production line activation time constraint
prob += 57 * y1 <= 22, "Activation_Time_A1"

# Solve the problem
prob.solve()

# Print the results
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Total Revenue: ${pulp.value(prob.objective)}")

# Display the solution
print(f"x1 (A1): {pulp.value(x1)}")
print(f"x2 (A2): {pulp.value(x2)}")
print(f"x3 (A3): {pulp.value(x3)}")
print(f"y1 (A1): {pulp.value(y1)}")
print(f"y2 (A2): {pulp.value(y2)}")
print(f"y3 (A3): {pulp.value(y3)}")