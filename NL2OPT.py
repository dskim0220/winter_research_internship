import os
import torch
import requests
import time
import json
import subprocess
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

from experts.BasicModelInterpreter import BasicModelInterpreter
from experts.ConstraintsInterpreter import ConstraintsInterpreter
from experts.Evaluator import Evaluator
from experts.Coder import Coder
from experts.InstanceDataSetGenerator import InstanceDataSetGenerator

#설정부분
model_name= "qwen2.5:32b"
url = "http://localhost:11434/api/generate"
data_set='newset'
problem_name='IndustryOR_21'
max_trial = 3
threshold=0.8

def save_output(content, filename, extension):
    file_path = f"output/{filename}.{extension}"

    with open(file_path,"w",encoding="utf-8") as f:
        if extension == "json":
            try:
                data = json.loads(content)
                json.dump(data,f,indent=4,ensure_ascii=False)
            except:
                f.write(content)
        
        else:
            f.write(content)
    
    print(f"[*] {file_path} 저장 완료")
    return file_path

def nl2opt(problem,model_name,url):
    #start_time = time.time()

    feedback = ""
    best_formulation = ""
    best_confidence_score = -1.0

    basic_interpreter = BasicModelInterpreter(model_name=model_name,url=url)
    constraints_interpreter = ConstraintsInterpreter(model_name=model_name,url=url)
    evaluator = Evaluator(model_name=model_name,url=url,threshold=threshold)
    coder = Coder(model_name=model_name,url=url)
    instance_generator = InstanceDataSetGenerator(model_name=model_name,url=url)
    
    for i in range(max_trial):
        basic_interpretation = basic_interpreter.interpret(problem_description=problem,feedback=feedback)
        whole_interpretation = constraints_interpreter.interpret(problem_description=problem,basic_interpretation=basic_interpretation)
        
        model_file = save_output(whole_interpretation, f"{problem_name}_model_trial{i}","json")

        raw_feedback = evaluator.evaluate(problem_description=problem, whole_interpretation=whole_interpretation)
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
        
        instances = instance_generator.extract_instances(problem=problem,coder_output=code)
        instance_file = save_output(instances,f"{problem_name}_instances","json")
        print("인스턴스 데이터셋 생성 완료!")

    #end_time = time.time()
    #running_time = end_time - start_time
    print(f"총 소요시간: {running_time:.2f}s")
    return

def run_code(code_path, data_path):
    print("코드 실행 중...")
    try:
        result = subprocess.run(["python", code_path, "--data", data_path], capture_output=True, text=True,encoding='utf-8',timeout=30)
        if result.returncode == 0:
            print("코드 실행 성공!")
            return {
            "success": True,
            "log": result.stdout,
            "error": None
        }
        else:
            print("코드 실행 실패!")
            return {
            "success": False,
            "log": result.stdout,
            "error": result.stderr
        }
    except subprocess.TimeoutExpired:
        # 시간 초과 발생 시 처리
        return {
            "success": False, 
            "log": "", 
            "error": "Execution timed out (Limit: 30s). The model might be too complex or in an infinite loop."
        }

if __name__ == '__main__':
    from utils import read_problem2
    # 풀 문제 설정
    start_time = time.time()
    problem = read_problem2(data_set, problem_name)
    nl2opt(problem, model_name, url)
    execution_result = run_code(f"output/{problem_name}_gencode.py",f"output/{problem_name}_instances.json")
    print(f"결과: {execution_result}")
    end_time = time.time()
    running_time = end_time - start_time
    print(f"총 소요시간: {running_time:.2f}s")