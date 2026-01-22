from gurobipy import *

def optimize_delivery_cost():
    # Create a new model
    m = Model("logistics_optimization")
    
    # Define decision variables
    x = m.addVar(lb=10, ub=40, name="x")  # Trucks for GoodsX
    y = m.addVar(lb=15, ub=35, name="y")  # Trucks for GoodsY
    z = m.addVar(lb=0, ub=50-x-y, name="z")  # Trucks for GoodsZ
    o_x = m.addVar(lb=0, name="o_x")  # Optimization investment for GoodsX
    o_y = m.addVar(lb=0, name="o_y")  # Optimization investment for GoodsY
    o_z = m.addVar(lb=0, name="o_z")  # Optimization investment for GoodsZ
    
    # Objective function: Minimize total delivery cost
    m.setObjective(1000*x + 1200*y + 1500*z + 100*o_x*(1000-10*o_x) + 100*o_y*(1200-12*o_y) + 100*o_z*(1500-15*o_z), GRB.MINIMIZE)
    
    # Constraints
    m.addConstr(x + y + z <= 50, "Total_trucks_constraint")
    m.addConstr(o_x + o_y + o_z <= x + y + z, "Investment_constraint")
    m.addConstr(100*o_x + 100*o_y + 100*o_z <= 10000, "Budget_constraint")
    m.addConstr(1000*o_x + 1200*o_y + 1500*o_z <= 10000, "Cost_savings_constraint")
    m.addConstr(x >= 10, "Min_trucks_GoodsX")
    m.addConstr(y >= 15, "Min_trucks_GoodsY")
    
    # Optimize the model
    m.optimize()
    
    # Check if the solution is optimal
    if m.status == GRB.Status.OPTIMAL:
        print('Optimal Solution:')
        print(f'Trucks for GoodsX: {x.X}')
        print(f'Trucks for GoodsY: {y.X}')
        print(f'Trucks for GoodsZ: {z.X}')
        print(f'Optimized Investment in Optimization Software for GoodsX: {o_x.X}')
        print(f'Optimized Investment in Optimization Software for GoodsY: {o_y.X}')
        print(f'Optimized Investment in Optimization Software for GoodsZ: {o_z.X}')
        print(f'Minimum Total Delivery Cost: {m.objVal}')
    else:
        print('No optimal solution found.')

# Run the optimization
optimize_delivery_cost()