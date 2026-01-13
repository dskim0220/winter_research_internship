import gurobipy as gp
from gurobipy import GRB

def prob_0(DogCapability,TruckCapability,DogCost,TruckCost,MaxBudget):
    """
    Formulates and solves a Mixed-Integer Program (MIP) to maximize the number of fish
    transported, subject to budget and trip count constraints, using Gurobi.

    Args:
        DogCapability: an integer, indicates the amount of fish which sled dogs can take per trip
        TruckCapability: an integer, indicates the amount of fish which trucks can take per trip
        DogCost: an integer, indicates the cost per trip for a sled dog
        TruckCost: an integer, indicates the cost per trip for a truck
        MaxBudget: an integer, denotes the upper limit of the budget

    Returns:
        FishTransported: an integer, denotes the amount of fish transported after calculation.
                         Returns 0 if no feasible solution exists.
    """
    FishTransported = 0

    try:
        # Create a new model
        model = gp.Model("FisheryTransportation")

        # --- Decision Variables ---
        # Let x_s be the number of trips made by sled dogs
        # Let x_t be the number of trips made by trucks
        # Both variables must be non-negative integers.
        x_s = model.addVar(vtype=GRB.INTEGER, name="num_sled_dog_trips", lb=0)
        x_t = model.addVar(vtype=GRB.INTEGER, name="num_truck_trips", lb=0)

        # --- Objective Function ---
        # Maximize the total number of fish transported:
        # Maximize DogCapability * x_s + TruckCapability * x_t
        model.setObjective(DogCapability * x_s + TruckCapability * x_t, GRB.MAXIMIZE)

        # --- Constraints ---
        # 1. Budget Constraint: The total cost of all trips must not exceed the maximum allowed budget.
        #    DogCost * x_s + TruckCost * x_t <= MaxBudget
        model.addConstr(DogCost * x_s + TruckCost * x_t <= MaxBudget, "Budget_Constraint")

        # 2. Trip Count Relationship Constraint: The number of sled dog trips must be
        #    strictly less than the number of truck trips.
        #    x_s <= x_t - 1
        model.addConstr(x_s <= x_t - 1, "Trip_Count_Relationship_Constraint")

        # --- Optimize the model ---
        model.optimize()

        # --- Extract Results ---
        if model.status == GRB.OPTIMAL:
            # The objective value is the total fish transported.
            # It's cast to int as per the return type specification.
            FishTransported = int(model.objVal)
        elif model.status == GRB.INFEASIBLE:
            # If the model is infeasible, no fish can be transported under the given constraints.
            FishTransported = 0
        else:
            # Handle other statuses (e.g., UNBOUNDED, INTERRUPTED) by returning 0,
            # as no optimal feasible solution was found.
            FishTransported = 0

    except gp.GurobiError as e:
        # Catch Gurobi-specific errors and return 0.
        FishTransported = 0
    except Exception as e:
        # Catch any other unexpected errors and return 0.
        FishTransported = 0

    return FishTransported