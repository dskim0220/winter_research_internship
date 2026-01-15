import numpy as np
from gurobipy import *

def aircraft_landing(EarliestLanding, LatestLanding, TargetLanding, PenaltyAfterTarget, PenaltyBeforeTarget, SeparationTime):
    """
    Args:
        EarliestLanding: list of integers, earliest landing times for each aircraft.
        LatestLanding: list of integers, latest landing times for each aircraft.
        TargetLanding: list of integers, target landing times for each aircraft.
        PenaltyAfterTarget: list of integers, penalties for landing after target times for each aircraft.
        PenaltyBeforeTarget: list of integers, penalties for landing before target times for each aircraft.
        SeparationTime: 2D list of integers, separation times between each pair of aircraft.

    Returns:
        min_total_penalty: an integer, denotes the minimized total penalty after calculation.
    """
    # Convert lists to numpy arrays for easier manipulation
    EarliestLanding = np.array(EarliestLanding)
    LatestLanding = np.array(LatestLanding)
    TargetLanding = np.array(TargetLanding)
    PenaltyAfterTarget = np.array(PenaltyAfterTarget)
    PenaltyBeforeTarget = np.array(PenaltyBeforeTarget)
    SeparationTime = np.array(SeparationTime)

    # Number of aircraft
    n = len(EarliestLanding)

    # Create a model, and name it
    m = Model("Aircraft_Landing_Problem")

    # Create variables
    y = m.addVars(n, lb=EarliestLanding, ub=LatestLanding, vtype=GRB.CONTINUOUS, name="y")
    x = m.addVars(n, n, vtype=GRB.BINARY, name="x")

    # Set objective
    m.setObjective(sum(PenaltyBeforeTarget[i] * x[i, j] + PenaltyAfterTarget[i] * (1 - x[i, j]) for i in range(n) for j in range(n)), GRB.MINIMIZE)

    # Add constraints
    # Order Constraint
    for i in range(n):
        for j in range(i+1, n):
            m.addConstr(x[i, j] + x[j, i] <= 1)

    # Separation Constraint
    for i in range(n):
        for j in range(i+1, n):
            m.addConstr(y[i] - y[j] >= SeparationTime[i, j] + 1e6 * (1 - x[i, j]))

    # Time Window Constraints
    for i in range(n):
        m.addConstr(EarliestLanding[i] <= y[i])
        m.addConstr(y[i] <= LatestLanding[i])

    # Solve the model
    m.optimize()

    # Calculate the total penalty
    min_total_penalty = sum(PenaltyBeforeTarget[i].x * x[i, j].x + PenaltyAfterTarget[i].x * (1 - x[i, j]).x for i in range(n) for j in range(n))

    return int(min_total_penalty)