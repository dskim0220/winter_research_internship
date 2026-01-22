import pulp

# Define the problem
problem = pulp.LpProblem("Manufacturing_Demand_Satisfaction", pulp.LpMinimize)

# Define decision variables
y1, y2, y3, y4 = pulp.LpVariable('y1', lowBound=0, cat='Continuous')
x1, x2, x3, x4 = pulp.LpVariable(('x1', 'x2', 'x3', 'x4'), lowBound=0, cat='Binary')

# Objective function
problem += y1 + y2 + y3 + y4, "Total_Hours"

# Constraints
problem += 10*y1 + 8*y2 + 6*y3 + 5*y4 >= 1000, "Smartphones_Demand"
problem += 5*y1 + 6*y2 + 7*y3 + 8*y4 >= 800, "Tablets_Demand"
problem += 3*y1 + 4*y2 + 5*y3 + 6*y4 >= 600, "Laptops_Demand"
problem += x1 + x2 + x3 + x4 <= 4, "Max_Operational_Lines"
problem += x1 + x2 + x3 + x4 >= 1, "At_least_one_line_operational"
problem += y1 <= 20*x1, "Line_1_Workers"
problem += y2 <= 20*x2, "Line_2_Workers"
problem += y3 <= 20*x3, "Line_3_Workers"
problem += y4 <= 20*x4, "Line_4_Workers"
problem += 20*(x1 + x2 + x3 + x4) <= 50, "Worker_Demand"
problem += x1 <= 1, "Line_1_Binary"
problem += x2 <= 1, "Line_2_Binary"
problem += x3 <= 1, "Line_3_Binary"
problem += x4 <= 1, "Line_4_Binary"

# Solve the problem
status = problem.solve()

# Check if the problem was solved successfully
if pulp.LpStatus[status] == 'Optimal':
    print(f"Optimal Solution Found: {pulp.LpStatus[status]}")
    print(f"Minimum Hours Required: {pulp.value(problem.objective)}")
    print(f"Operational Lines: {x1.varValue}, {x2.varValue}, {x3.varValue}, {x4.varValue}")
    print(f"Hours on Line 1: {y1.varValue}, Line 2: {y2.varValue}, Line 3: {y3.varValue}, Line 4: {y4.varValue}")
else:
    print("No optimal solution found.")