from pulp import *

# Create a LP Minimization Problem
prob = LpProblem("Warehouse_Planning", LpMinimize)

# Decision Variables
x_NY = LpVariable('x_NY', cat='Binary')
x_LA = LpVariable('x_LA', cat='Binary')
x_Ch = LpVariable('x_Ch', cat='Binary')
x_At = LpVariable('x_At', cat='Binary')
y_NY_LA = LpVariable('y_NY_LA', cat='Binary')
z_NY = LpVariable('z_NY', cat='Binary')
z_LA = LpVariable('z_LA', cat='Binary')
z_Ch = LpVariable('z_Ch', cat='Binary')
z_At = LpVariable('z_At', cat='Binary')

# Objective Function
prob += (
    20 * (80*x_NY + 70*x_LA + 40*x_Ch + 40*x_At) +
    48 * (80*x_NY + 70*x_LA + 40*x_Ch + 50*x_At) +
    26 * (80*x_NY + 70*x_LA + 40*x_Ch + 35*x_At) +
    50 * (80*x_NY + 70*x_LA + 40*x_Ch + 35*x_At) +
    400*z_NY + 500*z_LA + 300*z_Ch + 150*z_At
), "Total Cost"

# Constraints
prob += x_NY + x_LA - y_NY_LA <= 1, "NY_LA_Constraint"
prob += x_NY + x_LA + x_Ch + x_At <= 2, "Two_Warehouses_Constraint"
prob += x_At + x_LA - z_NY <= 1, "Atlanta_LosAngeles_Constraint"
prob += x_NY + x_At <= 1, "NY_At_Limitation"
prob += z_NY + z_LA + z_Ch + z_At >= 1, "One_Warehouse_Constraint"
prob += z_NY + z_Ch <= 1, "NY_Ch_Limitation"
prob += 80*x_NY + 70*x_LA + 40*x_Ch + 40*x_At <= 100*x_NY + 100*x_LA + 100*x_Ch + 100*x_At, "Demand_Region1"
prob += 80*x_NY + 70*x_LA + 40*x_Ch + 50*x_At <= 100*x_NY + 100*x_LA + 100*x_Ch + 100*x_At, "Demand_Region2"
prob += 80*x_NY + 70*x_LA + 40*x_Ch + 35*x_At <= 100*x_NY + 100*x_LA + 100*x_Ch + 100*x_At, "Demand_Region3"

# Solve the model
status = prob.solve()

# Print the status of the solution
print(f"Status: {LpStatus[prob.status]}")

# Print the values of the decision variables
print(f"x_NY: {value(x_NY)}")
print(f"x_LA: {value(x_LA)}")
print(f"x_Ch: {value(x_Ch)}")
print(f"x_At: {value(x_At)}")
print(f"y_NY_LA: {value(y_NY_LA)}")
print(f"z_NY: {value(z_NY)}")
print(f"z_LA: {value(z_LA)}")
print(f"z_Ch: {value(z_Ch)}")
print(f"z_At: {value(z_At)}")

# Print the total cost
print(f"Total Cost: {value(prob.objective)}")