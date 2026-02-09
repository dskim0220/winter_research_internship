import os
import torch
import requests
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
class Coder():
    def __init__(self,model_name,url):
        self.url = url
        self.model_name = model_name
        self.role_description = ''
        self.task = ''
        self.rules = ''
        self.output_format = ''
        
    def generate(self,formulation):
        full_prompt = f"""[Role] {self.role_description}
[Whole Interpretation] {formulation}
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
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"Error: {e}"