import gurobipy as gp
from gurobipy import GRB

def prob_1():
    # 모델 생성
    model = gp.Model("printer_production")

    # 변수 정의
    x = model.addVar(lb=0, ub=20, vtype=GRB.CONTINUOUS, name="color_printers")
    y = model.addVar(lb=0, ub=30, vtype=GRB.CONTINUOUS, name="bw_printers")

    # 목적함수: 최대 이익
    model.setObjective(200 * x + 70 * y, GRB.MAXIMIZE)

    # 공용 기계 제약
    model.addConstr(x + y <= 35, name="machine_capacity")

    # 최적화 실행
    model.optimize()

    # 결과 반환
    if model.status == GRB.OPTIMAL:
        return int(model.objVal)
    else:
        return None


# 실행 예시
print(prob_1())
