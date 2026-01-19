import os
import json
from experts.natural_maker import NaturalMaker
from experts.LaTeX_maker import LaTeXMaker
from experts.code_generator import CodeGenerator

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

def end_to_end


