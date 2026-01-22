import pulp

# Problem definition
prob = pulp.LpProblem("Product_Production_Problem", pulp.LpMaximize)

# Decision variables
x1 = pulp.LpVariable.dicts('x1', range(1, 23), lowBound=20, cat='Continuous')
x2 = pulp.LpVariable.dicts('x2', range(1, 23), lowBound=20, cat='Continuous')
x3 = pulp.LpVariable.dicts('x3', range(1, 23), lowBound=16, cat='Continuous')

# Objective function
prob += pulp.lpSum([124*x1[d] + 109*x2[d] + 115*x3[d] for d in range(1, 23)]) - 170000 - 150000 - 100000, "Total_Revenue"

# Constraints
for d in range(1, 23):
    prob += x1[d] + x2[d] + x3[d] <= 5300 + 4500 + 5400, f"Production_Day_{d}"

for d in range(1, 23):
    prob += x1[d] <= 500, f"Prod_Qty_A1_Day_{d}"
    prob += x2[d] <= 450, f"Prod_Qty_A2_Day_{d}"
    prob += x3[d] <= 550, f"Prod_Qty_A3_Day_{d}"

# Solve the problem
prob.solve()

# Print results
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Total Revenue: ${pulp.value(prob.objective)}")

for v in prob.variables():
    print(f"{v.name}: {v.varValue}")

for d in range(1, 23):
    print(f"Day {d}: A1={x1[d].varValue}, A2={x2[d].varValue}, A3={x3[d].varValue}")