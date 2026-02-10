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
        self.role_description = 'Your mission is to generate a Python script that is 100 percents executable without any external data dependencies.'
        self.task = 'Translate the provided formulation into a standalone, executable Gurobi Python script.'
        
        self.rules = """[STRICT RULES]
1. LITERAL CODING: Do NOT use abstract loops or symbolic placeholders (e.g., `params["A1"]`). Hard-code every value.
2. SOURCE MAPPING: 
   - Logic: Use the 'LaTeX' field as the mathematical blueprint.
   - Numbers: Use the 'query' field to extract exact numerical values (e.g., 170000, 124).
3. DATA SECTION: Define all parameters as Python constants at the top of the script.
4. UNIT SYNC: Perform necessary unit conversions (e.g., tons to kg) based on the 'query' context before defining constants.
5. NO PARSING: The script must not contain any JSON loading or parsing logic. It must be 100 percents self-contained.
[Output Rules]
1. Respond ONLY with the executable Python code block.
2. No introductory or concluding text.
3. Use double backslashes (\\\\) for any internal string-based LaTeX if necessary.
4. Translate all mathematical logic from the JSON formulation precisely into Gurobi API.
"""
        
        self.output_format = """
import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
# Define numerical values from the problem description here.

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Sets & Indices
# Define range or list for sets.

# 4. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)
# Implement based on Decision Variables JSON.

# 5. Objective (LaTeX structure + query numbers)
# Implement using m.setObjective().

# 6. Constraints (LaTeX structure + query numbers)
# Implement using m.addConstr() or m.addConstrs().
# Ensure Big-M values are large enough (e.g., 1e6) if logic requires.

# 7. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    print(f"Optimal Objective Value: {m.objVal}")
    for v in m.getVars():
        if v.x > 1e-6:
            print(f"{v.varName}: {v.x}")
else:
    print("Optimization was not successful.")
"""
        
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
        print("model generation 요청중...")
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"model generation 실패: {e}"