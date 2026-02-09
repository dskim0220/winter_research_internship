import os
import torch
import requests
import time
import json
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

from experts.BasicModelInterpreter import BasicModelInterpreter
from experts.ConstraintsInterpreter import ConstraintsInterpreter
from experts.Evaluator import Evaluator
from experts.Coder import Coder
from E2E import save_output

#설정부분
model_name= "qwen2.5:32b"
url = "http://localhost:11434/api/generate"
data_set='newset'
problem_name='Optibench_234'
max_trial = 3
threshold=0.8

def nl2opt(problem,model_name,url):
    start_time = time.time()

    feedback = ""
    best_formulation = ""
    best_confidence_score = -1.0

    basic_interpreter = BasicModelInterpreter(model_name=model_name,url=url)
    constraints_interpreter = ConstraintsInterpreter(model_name=model_name,url=url)
    evaluator = Evaluator(model_name=model_name,url=url,threshold=threshold)
    coder = Coder(model_name=model_name,url=url)
    
    for i in range(max_trial):
        basic_interpretation = basic_interpreter.interpret(problem_description=problem,feedback=feedback)
        whole_interpretation = constraints_interpreter.interpret(problem_description=problem,basic_interpretation=basic_interpretation)
        
        model_file = save_output(whole_interpretation, f"{problem_name}_model_trial{i}","json")

        raw_feedback = evaluator.evaluate(problem = problem, whole_interpretation=whole_interpretation)
        refined_feedback = evaluator._extract_json(raw_feedback).replace('\\','\\\\')
        feedback = refined_feedback

        feedback_file = save_output(feedback,f"{problem_name}_feedback_trial{i}","json")
        data = json.loads(feedback)
        confidence_score = data.get('CONFIDENCE_SCORE',0.0)

        if confidence_score >= threshold:
            best_formulation = whole_interpretation
            best_confidence_score = confidence_score
            break
        
        elif confidence_score >= best_confidence_score:
            best_formulation = whole_interpretation
            best_confidence_score = confidence_score

    if best_formulation:
        code = coder.generate(formulation=best_formulation)
        code_file = save_output(code,f"{problem_name}_gencode","py")
    
    print(f"모델링 및 코드 생성 완료! confidence:{best_confidence_score}")
    end_time = time.time()
    running_time = end_time - start_time
    print(f"총 소요시간: {running_time:.2f}s")
    return

if __name__ == '__main__':
    from utils import read_problem2
    # 풀 문제 설정
    problem = read_problem2(data_set, problem_name)
    nl2opt(problem, model_name, url)