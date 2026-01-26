import os
import json
from experts.natural_maker import NaturalMaker
from experts.LaTeX_maker import LaTeXMaker
from experts.code_generator import CodeGenerator
from experts.model_evaluator import ModelEvaluator
from custom_callback_qwen import get_llm, get_custom_callback

#설정부분
data_set='newset'
problem_name='IndustryOR_22'
max_trial = 3
confidence_standard=0.8

#결과 파일로 저장
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

#엔드투엔드 실행함수
def e2e(problem,model):
    natural_maker = NaturalMaker(model=model)
    natural_json = natural_maker.forward(problem=problem)
    natural_file = save_output(natural_json, problem_name+'_natural',"json")

    LaTeX_maker = LaTeXMaker(model=model)
    LaTeX_json = LaTeX_maker.forward(natural_json=natural_json)
    LaTeX_file = save_output(LaTeX_json,problem_name+'_LaTeX',"json")

    code_generator = CodeGenerator(model=model)
    code = code_generator.forward(LaTeX_json=LaTeX_json)
    code_file = save_output(code,problem_name+'_gencode',"py")

    return


def e2e_v2(problem,model):
    feedback = None
    best_LaTeX_json = None
    best_score = -1.0
    current_feedback = None

    for i in range(max_trial):
        try:
            natural_maker = NaturalMaker(model=model)
            if feedback is None or not isinstance(feedback,dict):
                current_feedback = ""
            else:
                current_feedback = (
                    f"Previous Score: {feedback.get('CONFIDENCE_SCORE', 'N/A')}\n"
                    f"Overall: {feedback.get('OVERALL_FEEDBACK', '')}\n"
                    f"Sets: {feedback.get('SETS_FEEDBACK', '')}\n"
                    f"Parameters: {feedback.get('PARAMETERS_FEEDBACK', '')}\n"
                    f"Variables: {feedback.get('VARIABLES_FEEDBACK', '')}\n"
                    f"Objective: {feedback.get('OBJECTIVE_FEEDBACK', '')}\n"
                    f"Constraints: {feedback.get('CONSTRAINTS_FEEDBACK', '')}\n\n"
                    "Instruction: Revise the optimization model by addressing each feedback point above."
                )
            
            natural_json = natural_maker.forward(problem=problem,feedback=current_feedback)
            natural_file = save_output(natural_json, f"{problem_name}_natural_trial{i}","json")

            LaTeX_maker = LaTeXMaker(model=model)
            LaTeX_json = LaTeX_maker.forward(natural_json=natural_json)
            LaTeX_file = save_output(LaTeX_json,f"{problem_name}_LaTeX_trial{i}","json")

            model_evaluator = ModelEvaluator(model=model)
            raw_feedback = model_evaluator.forward(problem=problem,LaTeX_json=LaTeX_json)
            #confidence_score = feedback['CONFIDENCE_SCORE']
            
            #피드백 가공
            if isinstance(raw_feedback, str):
                try:
                    refined_feedback = model_evaluator._extract_json(raw_feedback)
                    feedback = json.loads(refined_feedback)
                except Exception as e:
                    print(f"JSON 추출 실패: {e}")
                    feedback = {"CONFIDENCE_SCORE":0.0, "OVERALL_FEEDBACK":raw_feedback}
            else:
                feedback = raw_feedback
                
            feedback_file = save_output(feedback,f"{problem_name}_feedback_trial{i}","json")
            confidence_score =feedback.get('CONFIDENCE_SCORE',0.0)

            if confidence_score >= confidence_standard:
                best_LaTeX_json = LaTeX_json
                best_score = confidence_score
                break
            elif confidence_score >= best_score:
                best_LaTeX_json = LaTeX_json
                best_score = confidence_score
        
        except Exception as e:
            print(f"{i}번째 시도 실패: {e}")
            feedback = None
            continue
    if best_LaTeX_json is not None:
        try:
            code_generator = CodeGenerator(model=model)
            code = code_generator.forward(LaTeX_json=best_LaTeX_json)
            code_file = save_output(code,f"{problem_name}_gencode","py")
            print(f"코드 생성 성공! 시도 횟수: {i} best score:{best_score}")
        except Exception as e:
            print(f"코드 생성 실패: {e}")
    else:
        print(f"모델 생성 실패 문제:{problem_name}, 시도: {max_trial}")
    return

if __name__ == '__main__':
    from utils import read_problem2
    # 풀 문제 설정
    problem = read_problem2(data_set, problem_name)
    e2e_v2(problem, model ='Qwen/Qwen2.5-3B-Instruct')


#일단 코드 맞게 나옴
