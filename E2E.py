import os
import json
from experts.natural_maker import NaturalMaker
from experts.LaTeX_maker import LaTeXMaker
from experts.code_generator import CodeGenerator
from custom_callback_qwen import get_llm, get_custom_callback

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

def e2e(problem,model):
    natural_maker = NaturalMaker(model=model)
    natural_json = natural_maker.forward(problem=problem)
    natural_file = save_output(natural_json, "natural_json","json")

    LaTeX_maker = LaTeXMaker(model=model)
    LaTeX_json = LaTeX_maker.forward(natural_json=natural_json)
    LaTeX_file = save_output(LaTeX_json,"LaTeX_json","json")

    code_generator = CodeGenerator(model=model)
    code = code_generator.forward(LaTeX_json=LaTeX_json)
    code_file = save_output(code,"generated_code","py")

    return


if __name__ == '__main__':
    from utils import read_problem
    # 풀 문제 설정
    problem = read_problem('LPWP', 'prob_1')
    e2e(problem, model ='Qwen/Qwen2.5-3B-Instruct')


#일단 코드 맞게 나옴
