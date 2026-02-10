import os
import torch
import requests
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
class ConstraintsInterpreter():
    def __init__(self,model_name,url):
        self.url = url
        self.model_name = model_name
        self.role_description = 'Your task is to take a basic mathematical formulation and refine the constraints section with extreme precision.'
        self.task = """
Review the provided problem description and the initial basic interpretation. 
Your task is to exhaustively identify and refine all mathematical constraints. 
For each constraint, you must specify its 'type', the 'indices' it covers, and the 'variables' and 'parameters' it 'involves', as per the required JSON schema. 
Ensure the logic is complete and ready for code implementation.
"""
        self.rules = """[STRICT MODELING RULES]
1. INDICATOR ALGEBRA: 
   - If a rule says "If A then B", use: $y_B \ge y_A$ (Binary logic).
   - If a rule says "If A, then $x \ge \text{{Value}}$", use: $x \ge \text{{Value}} \cdot y_A$ (Linking logic).
2. INDEX CONSISTENCY: Use clear indices (e.g., $i \in {{A, B, C}}$). Ensure all summations $\sum$ have explicit ranges.
3. DOMAIN DEFINITION: 
   - Binary: $y \in {{0, 1}}$
   - Integer: $x \in \mathbb{{Z}}^+$
   - Continuous: $x \ge 0$
4. BIG-M VALUE: If a maximum capacity is not given for Big-M, use $M = 10000$ and state it clearly.
5. NO LOOSE ENDS: Every parameter from the input must appear in either the Objective or Constraints.
[LOGICAL TEMPLATE]
- Goal: "Minimize cost" -> $\min \sum (\text{{Cost}}_i \cdot x_i)$
- Logic: "Selection forces minimum" -> $x_i \ge \text{{Min}}_i \cdot y_i$
- Logic: "Mutual exclusivity" -> $\sum y_i \le 1$
[Output Rules]
1. Response must be a single valid JSON object.
2. For all LaTeX commands, use double backslashes (\\\\) to prevent JSON encoding errors.
3. If basic_interpretation is provided, maintain its logic but refine/add the missing constraints details.
4. No additional text, explanations, or markdown blocks."""
        
        self.output_format = """
{
  "Set": [
    { "id": "I", "User Query": "Factories ...", "Latex Model": "I" }
  ],
  "Parameter": [
    { "id": "c", "User Query": "Transportation ...", "Latex Model": "c_{ij}", "index": ["i", "j"] }
  ],
  "Decision Variables": [
    { 
      "id": "x", 
      "User Query": "Amount ...", 
      "Latex Model": "x_{ij}", 
      "index": ["i", "j"], 
      "domain": "continuous", 
      "lower_bound": 0 
    }
  ],
  "Objective function": [
    { "id": "OBJ", "sense": "min", "User Query": "Minimize ...", "Latex Model": "\\\\min ..." }
  ],
  "Constraints": [
    { 
      "id": "C_cap", 
      "type": "capacity", 
      "User Query": "...", 
      "Latex Model": "...", 
      "index": ["i"], 
      "involves": { "variables": ["x"], "parameters": ["cap"] } 
    }
  ]
}
"""
        
    def interpret(self, problem_description,basic_interpretation):
        problem = problem_description
        full_prompt = f"""[Role] {self.role_description}
[Problem] {problem}
[Basic Interpretation] {basic_interpretation}
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
        print("constraints interpretation 요청중...")
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            print("constraints interpretation 완료!")
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"constraints interpretation 실패: {e}"