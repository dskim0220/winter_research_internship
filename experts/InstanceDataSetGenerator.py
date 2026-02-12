import os
import torch
import requests
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

class InstanceDataSetGenerator():
    def __init__(self, model_name, url):
        self.url = url
        self.model_name = model_name
        self.role_description = 'Expert Data Extractor for Mathematical Optimization.'
        self.task = """
1. Analyze the 'Generated Python Code' to identify all required keys in the 'params' and 'sets' dictionaries.
2. Cross-reference these keys with the 'Problem Description' to extract exact numerical values or list members.
3. Map each extracted value to its corresponding symbolic ID found in the code.
4. Ensure the output is a structured JSON that the generated script can immediately load and use.
"""
        self.rules = """[STRICT EXTRACTION RULES]
1. IDENTIFIER ALIGNMENT: The keys in your JSON output must EXACTLY match the IDs used in the Python code (e.g., if the code looks for data['parameters']['cost_A'], your key must be 'cost_A').
2. NUMERIC PRECISION: Extract values exactly as stated in the text. If the text says "at least 150", the parameter value is 150.
3. SET MAPPING: If a set 'I' is used for suppliers A, B, and C, create a list: ["A", "B", "C"].
4. BIG-M ASSIGNMENT: If the code requires a parameter 'M' but no specific limit is in the text, provide a sufficiently large value (e.g., 10000) and label it as 'M'.
5. NO CONVERSATION: Return only the JSON object. Do not include explanations about where the numbers came from.
"""
        self.output_format = """
{
    "parameters": {
        "cost_A": 120,
        "units_per_order": 20,
        "min_demand": 150,
        "M": 10000
    },
    "sets": {
        "I": ["A", "B", "C"],
        "J": ["Product1", "Product2"]
    }
}
"""
        
    
    def extract_instances_first(self, problem, coder_output):
        full_prompt = f"""[Role] {self.role_description}
[Original Problem] {problem}
[Coder Output] {coder_output}
[Task] {self.task}
[Rules] {self.rules}
[Format] {self.output_format}"""
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 2048   
            }
        }
        print("instance 추출중...")
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"model generation 실패: {e}"
    
    
    def extract_instances_second(self,problem,code_path):
        coder_output = ""
        try:
            with open(code_path,'r',encoding='utf-8') as f:
                coder_output = f.read()
            
        except FileNotFoundError:
            print("코드 파일을 찾을 수 없습니다. 인스턴스 추출 실패.")
            return
        
        print("파일 읽기 성공! 인스턴스 추출중....")
        
        full_prompt = f"""[Role] {self.role_description}
[Original Problem] {problem}
[Coder Output] {coder_output}
[Task] {self.task}
[Rules] {self.rules}
[Format] {self.output_format}"""
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 2048   
            }
        }
        print("instance 추출중...")
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"model generation 실패: {e}"
        